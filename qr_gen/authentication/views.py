from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from qr_gen import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from django.core.mail import EmailMessage, send_mail
import json
from django.http import JsonResponse
from django.views import View
from validate_email import validate_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# Create your views here.

@login_required(login_url='login')
def home(request):
    if request.method == "GET":
        return render(request, "index.html")

class signup(View):

    def post(self, request):
        username = request.POST.get("username")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")

        context = {
            'username': request.POST.get("username"),
            'fname' :request.POST.get("fname"),
            'lname' : request.POST.get("lname"),
            'email' : request.POST.get("email"),
            'pass1' : request.POST.get("pass1"),
        }
        
        #If Username exists
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(pass1) < 6:
                    messages.error(request, "Password too short")
                    return render(request, "authentication/signup.html", context)
        
                myuser = User.objects.create_user(username=username, email=email)
                myuser.set_password(pass1)
                myuser.first_name = fname
                myuser.last_name = lname
                myuser.is_active = False

                myuser.save()
                
                 #Welcome Email

        # subject = "Welcome to GFG - Django Login!!"
        # message = "Hello " + myuser.first_name + "!! \n" + "Welcome to GFG!! \n Thank you visiting our website \n We have also sent you a confirmation email, please confirm your email address in order to activate your account. \n\n Thank you"
        # from_email = settings.EMAIL_HOST_USER
        # to_list = [myuser.email]
        # send_mail(subject, message, from_email, to_list)

                #Email Address Confirmation

                current_site = get_current_site(request)
                email_subject = "Welcome to QR-GEN Login!!"
                message = render_to_string("email_confirmation.html", {
                    "name": myuser.first_name,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(myuser.pk)),
                    "token": generate_token.make_token(myuser)
                })

                email = EmailMessage(
                    email_subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email]
                )
                email.fail_silently = True
                email.send()

                messages.success(request, "Account created sucessfully")
                return render(request, "authentication/signup.html")

        return render(request, "authentication/signup.html")

    def get(self, request):
        return render(request, "authentication/signup.html")

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data["username"]

        if not str(username).isalnum():
            return JsonResponse({"username_error": "username should only contain alphanumeric characters"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error": "sorry username already exists"}, status=409)



        return JsonResponse({"username_valid": True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data["email"]

        if not validate_email(email):
            return JsonResponse({"email_error": "Email is invalid"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"username_error": "sorry email already exists"}, status=409)



        return JsonResponse({"email_valid": True})  

class FirstNameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        fname = data["fname"]

        if not str(fname).isalpha():
            return JsonResponse({"fname_error": "firstname should only contain alphabets"}, status=400)



        return JsonResponse({"fname_valid": True})

class LastNameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        lname = data["lname"]

        if not str(lname).isalpha():
            return JsonResponse({"lname_error": "lastname should only contain alphabets"}, status=400)



        return JsonResponse({"lname_valid": True})  

    

class loginView(View):

    def post(self, request):
        username = request.POST.get("username")
        pass1 = request.POST.get("pass1")

        if username and pass1:

            user = authenticate(username=username, password=pass1)

            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    fname = user.first_name
                    messages.success(request, f"Welcome {fname}, You are now logged in")
                    return redirect("home")
                    
            
                messages.error(request, "Account is not active, please check your email")
                return render(request, 'authentication/login.html')

            messages.error(request, "username/password is incorrect")
            return render(request, 'authentication/login.html')

        messages.error(request, "Please fill all fields")
        return render(request, 'authentication/login.html')
    
    def get(self, request):

        return render(request, "authentication/login.html")

# def logout(request):
#     auth_logout(request)
#     messages.success(request, "Logged Out Successfully")
#     return redirect("home")

class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            myuser = User.objects.get(pk=uid)
        
            if not generate_token.check_token(myuser, token):
                return redirect("login"+'?message='+'User already activated')

            if myuser.is_active:
                return redirect("login")
            myuser.is_active = True
            myuser.save()

            messages.success(request, "Account activated successfully")
            return redirect("login")
        
        except Exception as ex:
            pass

        return redirect("login")

class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')

    def post(self, request):
        email = request.POST.get("email")

        context = {
            'email' : request.POST.get("email"),
        }

        if not validate_email(email):
            messages.error(request, "Email is not valid")
            return render(request, "authentication/reset-password.html", context)

        current_site = get_current_site(request)
        user = request.objects.filter(email=email)
        if user.exists():
            email_subject = "Reset Password"
            message = render_to_string("reset_password_email.html", {
                        "name": user[0],
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user[0].pk)),
                        "token": PasswordResetTokenGenerator().make_token(user[0])
                    })

            email = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )
            email.fail_silently = True
            email.send()   
        
        messages.success(request, "Email has been to sent to reset your password")

        

        return render(request, "authentication/reset-password.html")


class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        return render(request, 'authentication/set-newpassword.html')

    def get(self, request, uidb64, token):
        return render(request, 'authentication/set-newpassword.html')