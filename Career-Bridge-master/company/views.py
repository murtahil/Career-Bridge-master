from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
import datetime
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q

# for email sending
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError

# rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from project.forms import RegisterProject
from project.models import Project, Milestones, Rating
from .models import Company
from university.models import Bidding, University, Service
from accounts.models import User
from project.forms import SignMouForm
from .forms import ChangeLogoForm

# Create your views here.
def index(request):
    #user validation start
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.user.user_type == 1:
        return redirect("/university/home")
    #user validation end
    try:
        company = Company.objects.get(admin=request.user.pk)
        request.session["logo"] = company.logo.url
    except Exception as identifier:
        request.session["logo"] = settings.MEDIA_URL + 'logos/defaultdp.jpg'
    company = Company.objects.get(admin=request.user.pk)
    projects = Project.objects.filter(developed_for=company, developed_by__isnull=False)
    context = {"projects": projects}
    return render(request, 'company/index.html', context)

def add_new_project(request):
    #user validation start
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.user.user_type == 1:
        return redirect("/university/home")
    #user validation end
    if request.method == 'POST':
        form = RegisterProject(request.POST)
        if form.is_valid():
            admin = Company.objects.get(admin=request.user.pk)
            project = Project(
                project_name = form.cleaned_data['project_name'],
                project_description= form.cleaned_data['project_description'],
                developed_for = admin,
                start_date= form.cleaned_data['start_date'],
                end_date= form.cleaned_data['end_date'],
                bidding_start= form.cleaned_data['bidding_start'],
                bidding_end= form.cleaned_data['bidding_end'],

                )
            project.save()
            messages.info(request, f"Project ' {project.project_name} ' pushed successfully!")
            return redirect('/company/home')
            # return render(request, 'company/index.html', context)
        else:
            context = {"form": form}
            return render(request, 'company/add_new_project.html', context)
    form = RegisterProject()
    context = {"form": form}
    return render(request, 'company/add_new_project.html', context)

def my_projects(request):
    #user validation start
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.user.user_type == 1:
        return redirect("/university/home")
    #user validation end
    admin = Company.objects.get(admin=request.user.pk)
    projects = Project.objects.filter(developed_for=admin, is_deleted=False).order_by("-created_at")    
    context = {"projects": projects}
    return render(request, "company/myproject.html", context)

def projet_details(request, project_id):
    #user validation start
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.user.user_type == 1:
        return redirect("/university/home")
    #user validation end
    admin = Company.objects.get(admin=request.user.pk)
    try:
        project = Project.objects.get(pk=project_id, developed_for=admin.pk)
        biddings = Bidding.objects.filter(project=project).order_by('bidding_price')
        highest_bidder = None
        if biddings:
            highest_bidder = University.objects.get(pk=biddings[0].bidder.pk)
            highest_bidding_user = User.objects.get(pk=highest_bidder.admin.pk)
        context = {"project": project, "biddings": biddings, "highest_bidder": highest_bidder}
        return render(request, "company/projet_details.html", context)
    except:
        pass   
    return render(request, "company/projet_details.html")

def end_auction(request, project_id):
    #user validation start
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.user.user_type == 1:
        return redirect("/university/home")
    #user validation end
    now = timezone.now()
    project = Project.objects.get(pk=project_id)
    project.bidding_end = now
    project.save()
    return redirect(f'/company/projet_details/{project.pk}/')

def start_deal(request, project_id, university_id):
    #user validation start
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.user.user_type == 1:
        return redirect("/university/home")
    #user validation end

    project = Project.objects.get(pk=project_id)
    university = University.objects.get(pk=university_id)
    company = Company.objects.get(admin=request.user.pk)
    project.company_deal=True
    project.save()

    current_site = get_current_site(request)
    subject = f"Start your project with {company.admin.fullname}"
    message = render_to_string(
        'company/start_deal.html',
        {
            'domain': current_site,
            'company_id': urlsafe_base64_encode(force_bytes(company.pk)),
            'project_id': urlsafe_base64_encode(force_bytes(project.pk)),
            'university_name': university.admin.fullname,
            'company_name': company.admin.fullname,
            'project_name': project.project_name,
        }
    )
    try:
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [university.admin.email]
        )
        email.send(fail_silently=False)
        messages.info(request, f"{university.name} is notified via email about your deal. Wait for their response!")
        return redirect(f"/company/projet_details/{project_id}")
    except Exception as identifier:
        messages.info(request, f"Network error. Please try again!")
        return redirect(f"/company/projet_details/{project_id}")
    
def confirm_deal(request, project_id, company_id):
    project_id =force_text(urlsafe_base64_decode(project_id))
    company_id =force_text(urlsafe_base64_decode(company_id))
    return redirect(f'/university/confirm_deal/{project_id}/{company_id}')
    return

def sign_mou(request, project_id):
    #user validation start
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.user.user_type == 1:
        return redirect("/university/home")
    #user validation end

    if request.method == "POST":
        user = User.objects.get(pk=request.user.pk)
        project = Project.objects.get(pk=project_id)
        university = University.objects.get(pk=project.developed_by.pk)
        company = Company.objects.get(admin=request.user.pk)
        form = SignMouForm(request.POST, request.FILES, instance=project)
        collab = form.save(commit=False)
        filename = form.cleaned_data.get("company_mou").name
        if not isFileValid(filename):
            messages.info(request, "Invalid file type. Please upload pdf, jpg or png file!")
            university = University.objects.get(pk=university.pk)
            context = {"university": university, "form": form}
            return render(request, 'company/sign_mou.html', context)
        collab.project = project
        collab.university = university
        collab.company = company
        collab.save()
        messages.info(request, "That's it now you can see milestones!")
        return redirect(f'/company/milestones/{project.pk}')        
    
    form = SignMouForm()
    project = Project.objects.get(pk=project_id)
    university = University.objects.get(pk=project.developed_by.pk)
    context = {"university": university, "form": form}
    return render(request, 'company/sign_mou.html', context)

def isFileValid(filename):
    extensions = ['pdf', 'jpg', 'jpeg', 'png']
    f = filename.lower()
    for ext in extensions:
        if f.endswith(ext):
            return True
    return False

def confirm_mou(request, project_id, company_id):    
    try:
        project_id =force_text(urlsafe_base64_decode(project_id))
        company_id =force_text(urlsafe_base64_decode(company_id))
        print(project_id ,company_id)
        return redirect(f'/university/confirm_mou/{project_id}/{company_id}')

    except Exception as identifier:
        pass

    return redirect('/company/home')

def profile(request, user_id):
    #user validation start
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.user.user_type == 1:
        return redirect(f"/university/profile/{user_id}")
    #user validation end

    if request.method == "POST":
        company = Company.objects.filter(admin=request.user.pk).first() 
        form = ChangeLogoForm(request.POST or None, request.FILES or None, instance=company)        
        if form.is_valid():
            form.save(commit=False)  
            filename = form.cleaned_data.get("logo").name
            if not isLogoValid(filename):
                messages.info(request, "Invalid file type. Please upload pdf or png file!")
                return redirect(f"/company/profile/{user_id}")
            form.save()
            user = User.objects.filter(pk=user_id).update(is_new=False)
            company = Company.objects.get(admin=request.user.pk)
            request.session["logo"] = company.logo.url
            return redirect(f"/company/profile/{user_id}")
        else:           
            return redirect(f"/company/profile/{user_id}")

    user = User.objects.get(pk=user_id)
    if user.user_type == 2:
        company = Company.objects.get(admin=user)
        projects = Project.objects.filter(developed_for=company, is_deleted=False).order_by("-created_at")
        context = {"user": user, "company": company, "projects": projects}
        if user_id == request.user.pk:
            context["isPersonal"] = True
            form = ChangeLogoForm()
            context["form"] = form            
        return render(request, "company/profile.html", context)
    elif user.user_type == 1:
        university = University.objects.get(admin=user)
        projects = Project.objects.filter(developed_by=university, is_deleted=False).order_by("-created_at")
        services = Service.objects.filter(university=university)

        context = {
            "user": user, 
            "university": university, 
            "projects": projects, 
            "services": services
        }

        return render(request, "company/profile.html", context)

    return render(request, "university/profile.html")

def isLogoValid(filename):
    extensions = ['jpg', 'jpeg', 'png']
    f = filename.lower()
    for ext in extensions:
        if f.endswith(ext):
            return True
    return False

def update_info(request):
    #user validation start
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.user.user_type == 1:
        return redirect("/university/home")
    #user validation end

    if request.method == "POST":
        name = request.POST["name"]
        address = request.POST["address"]
        contact = request.POST["phone"]
        website = request.POST["website"]

        try:
            user = User.objects.get(pk=request.user.pk)
            company = Company.objects.get(admin=user)
            user.phone = contact
            user.fullname = name
            user.website = website
            company.address = address
            company.name = name
            user.save()
            company.save()            
        except Exception as e:
            messages.info(request, "This contact number already exists. try another one!")
            return redirect(f"/company/profile/{request.user.pk}")
    
    return redirect(f"/company/profile/{request.user.pk}")

def search(request):
    search = request.GET["search"]
    companies = Company.objects.filter(Q(name__icontains=search)).order_by("-created_at")[:25]
    universities = University.objects.filter(Q(name__icontains=search)).order_by("ranking")[:25]
    services = Service.objects.filter(Q(service_name__icontains=search)).distinct("university")[:25]
    context = {"companies": companies, "universities": universities, "services": services, "last_search": search}
    return render(request, "company/search.html", context)

def active_projects(request):
    if request.method == "POST":
        project_id = request.POST["project_id"]
        q1 = request.POST["q1"]
        q2 = request.POST["q2"]
        q3 = request.POST["q3"]
        q4 = request.POST["q4"]
        feedback = request.POST["feedback"]
        project = Project.objects.get(pk=project_id)
        ratings = Rating.objects.filter(project=project)
        if ratings.exists():
            ratings.delete()
        rating = Rating(
            project = project,
            q1=q1, q2=q2, q3=q3, q4=q4,
            feedback=feedback,
            rating=float(int(q1) + int(q2) + int(q3) + int(q4)) / float(4)
        )
        rating.save()
        university = University.objects.get(pk=project.developed_by.pk)
        projects = Project.objects.filter(developed_by=university.pk, is_completed=True)
        ratings = Rating.objects.filter(project__in =projects)
        sum = 0
        for rat in ratings:
            sum += rat.rating
        ranking = sum /ratings.count()
        university.ranking = ranking
        university.save()
        messages.info(request, "Thanks for your feedback!")

    company = Company.objects.get(admin=request.user.pk)
    projects = Project.objects.filter(developed_for=company, developed_by__isnull=False).order_by("-created_at")
    context = {"projects": projects}
    return render(request, "company/activeprojects.html", context)

def milestones(request, project_id):
    project = Project.objects.get(pk=project_id)
    milestones = Milestones.objects.filter(project=project).order_by('start_date')
    context = {"project": project, "milestones": milestones}
    if project.company_mou:
        context["isMouSigned"] = True
    return render(request, "company/milestones.html", context)

def delete_projet(request):
    if request.method == "POST":
        project_id = request.POST["project_id"]
        project = Project.objects.get(pk=project_id)
        project.is_deleted = True
        project.save()
        messages.info(request, f"{project.project_name} is deleted!")
        return redirect("/company/my_projects")
    return redirect("/company/my_projects")

def mark_as_complete(request):
    if request.method == "POST":
        project_id = request.POST["project_id"]
        project = Project.objects.get(pk=project_id)
        project.is_completed = True
        project.save()
        messages.info(request, f"{project.project_name} is marked as complete!")
        return redirect("/company/active_projects")
    return redirect("/company/active_projects")

def mou_details(request, project_id):
    project = Project.objects.get(pk=project_id)
    context = {"project": project}
    return render(request, "company/mous.html", context)
