from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.db.models import Min, Max
from django.utils import timezone

# for email sending
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError

#rest framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from project.models import Project, Milestones
from .models import Bidding, University, Service
from company.models import Company
from .forms import SignMouForm, ChangeLogoForm, EditUserInfoForm, EditUniversityInfoForm, AddMilestoneForm
from accounts.models import User

# Create your views here.

def index(request):
    #user validation start
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.user.user_type == 2:
        return redirect("/company/home")
    #user validation end
    try:
        university = University.objects.get(admin=request.user.pk)
        request.session["logo"] = university.logo.url
    except Exception as identifier:
        request.session["logo"] = settings.MEDIA_URL + 'logos/defaultdp.jpg'
    
    admin = University.objects.get(admin=request.user.pk)
    projects = Project.objects.filter(developed_by=admin).order_by("-created_at")
    no_of_projects = Project.objects.all().count()
    no_of_companies = Company.objects.all().count()
    no_of_universities = University.objects.all().count()
    no_of_bids = Bidding.objects.all().count()
    context = {
        "no_of_projects": no_of_projects, 
        "no_of_companies": no_of_companies,
        "no_of_universities": no_of_universities,
        "no_of_bids": no_of_bids,
        "projects": projects
        }
    return render(request, 'university/index.html', context)

def active_projects(request):
    #user validation start
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.user.user_type == 2:
        return redirect("/company/home")
    #user validation end
    
    projects = Project.objects.filter(developed_by=None).order_by('-created_at')
    context = {"projects": projects}
    return render(request, 'university/activeprojects.html', context)

def project_details(request, project_id):
    #user validation start
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.user.user_type == 2:
        return redirect("/company/home")
    #user validation end
    
    if request.method == "POST":
        project_key = request.POST["project_id"]
        bidding_price = request.POST["bidding_price"]
        bidder = University.objects.get(admin=request.user.pk)
        project = Project.objects.get(pk=project_key)
        bid = Bidding.objects.filter(project=project, bidder=bidder).first()
        if bid:
            if bid.revisions == 2:
                project = Project.objects.get(pk=project_id)
                biddings = Bidding.objects.filter(project=project).order_by('bidding_price')
                context = {"project": project, "biddings": biddings,"revisionsCompleted": True}
                return render(request, 'university/project_details.html', context)
            bid.bidding_price = bidding_price
            bid.revisions = 2
            bid.save()
        else:
            bid = Bidding(
                bidder=bidder,
                project = project,
                bidding_price= bidding_price
            )
            bid.save()
        project = Project.objects.get(pk=project_id)
        biddings = Bidding.objects.filter(project=project).order_by('bidding_price')
        context = {"project": project, "biddings": biddings,"isBiddingDone": True}
        return render(request, 'university/project_details.html', context)

    project = Project.objects.get(pk=project_id)
    biddings = Bidding.objects.filter(project=project).order_by('bidding_price')
    return render(request, 'university/project_details.html', {"project": project, "biddings": biddings})

def confirm_deal(request, project_id, company_id):
    #user validation start
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.user.user_type == 2:
        return redirect("/company/home")
    #user validation end

    company = Company.objects.get(pk=company_id)
    project = Project.objects.get(pk=project_id)
    context = {"company": company, "project": project}
    return render(request, "university/confirm_deal.html", context)

def done_project_deal(request, project_id, company_id):
    #user validation start
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.user.user_type == 2:
        return redirect("/company/home")
    #user validation end

    project = Project.objects.get(pk=project_id, company_deal=True, developed_by=None)
    company = Company.objects.get(pk=company_id)
    university = University.objects.get(admin=request.user.pk)
    if project:
        project.developed_by=university
        if not project.is_bidding_ended():
            project.university_deal=True
        now = timezone.now()
        project.bidding_end = now
        project.save()
        subject = f"Deal Confirmation Message from {request.user.fullname}"
        message = f"Hi {company.name}!\n{request.user.fullname} has accepted your deal and soon they will start working on your project."
        try:
            email = EmailMessage(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [company.admin.email]
            )
            email.send(fail_silently=False)
            messages.info(request, f"Your deal is finalized with {company.name} for the project {project.project_name}. Now you can start the project by creating milestones!")
            return redirect("/university/home")
        except Exception as identifier:
            messages.info(request, f"A network error. Please try again!")
            return redirect('/company/home')
    else:
        messages.info(request, f"Sorry you are late. {company.name} has started deal with another university!")
        return redirect("/university/home")

def sign_mou(request, project_id):
    #user validation start
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.user.user_type == 2:
        return redirect("/company/home")
    #user validation end
    
    if request.method == "POST":
        university = University.objects.get(admin=request.user.pk)
        project = Project.objects.get(pk=project_id)
        company = Company.objects.get(pk=project.developed_for.pk)
        form = SignMouForm(request.POST or None, request.FILES or None, instance=project)
        form.save(commit=False)
        filename = form.cleaned_data.get("university_mou").name
        if not isFileValid(filename):
            messages.info(request, "Invalid file type. Please upload pdf, jpg or png file!")
            context = {"company": company, "project": project, "form": form}
            return render(request, "university/sign_mou.html", context)
        if form.is_valid():
            
            form.save()
            project.developed_by = university
            project.save()
            messages.info(request, "Ok! Now you can add milestones.")
            return redirect(f'/university/create_milestone/{project_id}')
            
        messages.info(request, "An internal error. Please try again!")
        return redirect(f'/university/create_milestone/{project_id}')

    project = Project.objects.get(pk=project_id)
    company = Company.objects.get(pk=project.developed_for.pk)
    form = SignMouForm()
    context = {"company": company, "project": project, "form": form}
    return render(request, "university/sign_mou.html", context)

def isFileValid(filename):
    extensions = ['pdf', 'jpg', 'jpeg', 'png']
    f = filename.lower()
    for ext in extensions:
        if f.endswith(ext):
            return True
    return False

def myprojects(request):
    admin = University.objects.get(admin=request.user.pk)
    projects = Project.objects.filter(developed_by=admin).order_by("-created_at")
    context = {"projects": projects}
    return render(request, "university/myprojects.html", context)

def profile(request, user_id):
    #user validation start
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.user.user_type == 2:
        return redirect(f"/company/profile/{user_id}")
    #user validation end

    if request.method == "POST":
        university = University.objects.filter(admin=request.user.pk).first() 
        form = ChangeLogoForm(request.POST or None, request.FILES or None, instance=university)
        
        if form.is_valid():
            form.save(commit=False)  
            filename = form.cleaned_data.get("logo").name
            if not filename.lower().endswith('jpg') and not filename.lower().endswith('png') and not filename.lower().endswith('jpeg'):
                messages.info(request, "Invalid file type. Please upload pdf or png file!")
                return redirect(f"/university/profile/{user_id}")
            form.save()
            user = User.objects.filter(pk=user_id).update(is_new=False)
            university = University.objects.get(admin=request.user.pk)
            request.session["logo"] = university.logo.url
            return redirect(f"/university/profile/{user_id}")
        else:
            for errors in  form.errors['__all__'].as_data():
                for error in errors:
                    messages.info(request, error)
            return redirect(f"/university/profile/{user_id}")

    try:
        user = User.objects.get(pk=user_id)    
    except Exception as e:
        messages.info(request, "Invalid User ID")
        return redirect(f"/university/home")
    if user.user_type == 1:
        university = University.objects.get(admin=user)
        services = Service.objects.filter(university=university)
        projects = Project.objects.filter(developed_by=university)

        context = {
            "user": user, 
            "university": university, 
            "projects": projects, 
            "services": services
        }
        if user.pk == request.user.pk:
            context["isPersonal"] = True
            form = ChangeLogoForm()
            context["form"] = form
            
        return render(request, "university/profile.html", context)
    elif user.user_type == 2:
        company = Company.objects.get(admin=user)
        projects = Project.objects.filter(developed_for=company)
        context = {"user": user, "company": company, "projects": projects}
        return render(request, "university/profile.html", context)

    else:
        return redirect("/login")


    return render(request, "university/profile.html")

def update_info(request):
    #user validation start
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.user.user_type == 2:
        return redirect("/company/home")
    #user validation end

    if request.method == "POST":
        name = request.POST["name"]
        address = request.POST["address"]
        contact = request.POST["phone"]
        website = request.POST["website"]

        try:
            user = User.objects.get(pk=request.user.pk)
            university = University.objects.get(admin=user)
            user.phone = contact
            user.fullname = name
            user.website = website
            university.address = address
            university.name = name
            user.save()
            university.save()            
        except Exception as e:
            messages.info(request, "This contact number already exists. try another one!")
            return redirect(f"/university/profile/{request.user.pk}")
    
    return redirect(f"/university/profile/{request.user.pk}")

def services(request):
    #user validation start
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.user.user_type == 2:
        return redirect("/company/home")
    #user validation end

    if request.method == "POST":
        university = University.objects.get(admin=request.user.pk)
        service_name = request.POST["service_name"]
        service = Service(university=university, service_name=service_name)
        service.save()
        services = Service.objects.filter(university=university)
        context = {"services": services}
        return render(request, "university/services.html", context)
   
    university = University.objects.get(admin=request.user.pk)
    services = Service.objects.filter(university=university)
    context = {"services": services}
    return render(request, "university/services.html", context)

def delete_service(request):
    if request.method == "POST":
        service_id = request.POST["service_id"]
        Service.objects.get(pk=service_id).delete()
        return redirect("/university/services")

def search(request):
    search = request.GET["search"]
    companies = Company.objects.filter(Q(name__icontains=search)).order_by("-created_at")[:25]
    universities = University.objects.filter(Q(name__icontains=search)).order_by("ranking")[:25]
    services = Service.objects.filter(Q(service_name__icontains=search)).distinct("university")[:25]
    context = {"companies": companies, "universities": universities, "services": services, "last_search": search}
    return render(request, "university/search.html", context)
 
def create_milestone(request, project_id):
    if request.method == 'POST':
        project = Project.objects.get(pk=project_id)
        name = request.POST['name']
        description = request.POST['description']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        milestone =  Milestones(name=name, description=description, project=project, start_date=start_date, end_date=end_date)
        milestone.save()
        messages.info(request, "Milestone added!")
        form = AddMilestoneForm()
        project = Project.objects.get(pk=project_id)
        milestones = Milestones.objects.filter(project=project)
        context = {"form": form, 'milestones': milestones, "isMouSigned": True}
        return render(request ,"university/create_milestone.html", context)
    form = AddMilestoneForm()
    project = Project.objects.get(pk=project_id)
    milestones = Milestones.objects.filter(project=project).order_by('start_date')
    context = {"form": form, 'milestones': milestones, "project_id": project_id }
    if project.university_mou:
        context["isMouSigned"] = True
    if project.is_completed:
        context["isProjectCompleted"] = True
    return render(request ,"university/create_milestone.html", context)

def delete_milestone(request):
    if request.method == "POST":
        milestone_id = request.POST["milestone_id"]
        milestone = Milestones.objects.get(pk=milestone_id)
        project = Project.objects.get(pk=milestone.project.pk)
        name = milestone.name
        milestone.delete()
        messages.info(request, f'Milestone \"{name}\" is deleted!')
        return redirect(f"/university/create_milestone/{project.pk}")
    return redirect("/university/home")

def mou_details(request, project_id):
    project = Project.objects.get(pk=project_id)
    context = {"project": project}
    return render(request, "university/mous.html", context)

class ListChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id', "1")
        user = User.objects.get(pk=user_id)
        result = Bidding.objects.values("project").annotate(min_bidding_price=Min('bidding_price'))
        
        labels = []
        def_data = []
        chart_label = "Bids"
        count = 0
        for r in result:
            project = Project.objects.get(pk=r['project'])
            labels.append("".join(word[0] for word in project.project_name.upper().split(" ")))
            def_data.append(r['min_bidding_price'])
            count += 1
            if count > 9:
                break

        data = { 
            "data": def_data,
            "labels": labels,
            "chart_label": chart_label
        }

        return Response(data)