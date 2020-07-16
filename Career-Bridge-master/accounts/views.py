from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as loginn, logout
from django.contrib.auth.models import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
# form emal sending
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .utils import generate_token

from .models import User, ContactUs
from university.models import University
from company.models import Company
from .forms import RegisterForm

# Create your views here.

def index(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        if "@" in email:
            contactUs = ContactUs(
                name=name,
                email=email,
                message=message
            )
            contactUs.save()
            context = {"isMessageSaved": True}
            return render(request, 'index.html', context)
        else:
            context = {"isMailInvalid": True}
            return render(request, 'index.html', context)
    return render(request, 'index.html')

def login(request):
    user = request.user
    if user.is_authenticated:
        if user.user_type == 1:
            return redirect('/university/home')
        elif user.user_type == 2:
            return redirect('/company/home')
        return redirect("/login")


    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)
        if user is not None:
            if not user.email_verify:
                return render(request, 'login.html', {"emailNotVerified": True})    
            auth.login(request, user)
            if user.user_type == 1:
                return redirect('/university/home')
            elif user.user_type == 2:
                return redirect('/company/home')
            else:
                messages.info(request, 'The User You Enter are not found')
                return redirect('/login')
        else:
            messages.info(request, 'invalid credential')
            return redirect('/login')
   
    return render(request, 'login.html')

def signup(request):
    #user validation start
    if request.user.is_authenticated:
        if request.user.user_type == 1:
            return redirect("/university/home")
        elif request.user.user_type == 2:
            return redirect("/company/home")
    #user validation end
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.user_type == 1:
                university = University(name=user.fullname, admin=user)
                university.save()
            else:
                company = Company(name=user.fullname, admin=user )
                company.save()
            curren_site = get_current_site(request)
            subject = "Activate your Career Bridge account"

            message = render_to_string(
                'auth/activate.html',
                {
                    'user': user,
                    'domain': curren_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user)
                }
                )

            email = EmailMessage(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            email.send(fail_silently=False)

            context = {"isSignedUp": True, "name": form.cleaned_data['fullname']}
            return render(request, 'login.html', context)            
        else:
            context = {"form": form}
            return render(request, 'signup.html', context)

    form = RegisterForm()
    context = {"form": form}
    return render(request, 'signup.html', context)

def activate_account(request, uidb64, token):
    try:
        uid =force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as identifier:
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.email_verify=True
        user.save()
        context = {"isActivated": True}
        return render(request, "login.html", context)
    return render(request, 'auth/activate_failed.html', status=401)

def logout_view(request):
    logout(request)
    return redirect("/index")

def change_password(request):
    user = request.user
    if not user.is_authenticated:
        messages.info(request, "First login to change password!")
        return redirect("/login")

    if request.method == "POST":
        old_password = request.POST["old"]
        new_password = request.POST["new"]
        confirm_new_password = request.POST["confirm_new"]        
        if new_password == confirm_new_password:
            if len(new_password) < 8:
                messages.info(request, "Password must be atleast 8 characters. Try again!")
                
            else:
                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    loginn(request, user)
                    messages.info(request, "Password changed successfully")
                    if user.user_type == 1:
                        return redirect("/university/home")
                    if user.user_type == 2:
                        return redirect("/company/home")
                else:
                    messages.info(request, "Incorrect old password. Try again!")
                    
        else:
            messages.info(request, "New passwords does not match. Try again!")
            
    return render(request, "change_password.html")
    
def reset_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        user = User.objects.filter(email=email).first()
        if not user:
            messages.info(request, "Email not found!")
            return render(request, "auth/reset_password.html")
        else:
            curren_site = get_current_site(request)
            subject = "Reset your Career Bridge password"

            message = render_to_string(
                'auth/reset_temp.html',
                {
                    'user': user,
                    'domain': curren_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user)
                }
                )

            email = EmailMessage(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            print(message)
            email.send(fail_silently=False)

            context = {"isResetMailSent": True, }
            return render(request, 'auth/reset_password.html', context)

    return render(request, "auth/reset_password.html")


def reset_the_password(request, uidb64, token):
    try:
        uid =force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as identifier:
        user = None

    if request.method == "POST":
        new_password = request.POST["new"]
        confirm_new_password = request.POST["confirm_new"]        
        if new_password == confirm_new_password:
            if len(new_password) < 8:
                messages.info(request, "Password must be atleast 8 characters. Try again!")
            else:
                user.set_password(new_password)
                user.save()
                messages.info(request, "Password Reset Successfully!")
                return redirect("/login")
        else:
            messages.info(request, "New passwords does not match. Try again!")
    if user is not None and generate_token.check_token(user, token):
        print(user.pk)
        context = {"isActivated": True}
        return render(request, "auth/new_password.html", context)
    return render(request, 'auth/activate_failed.html', status=401)