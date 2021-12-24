import random
import re
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from .auth import unauthenticated_user
from .forms import LoginForm
from django.contrib.auth.models import User
from .forms import UserRegisterForm
import json
from django.shortcuts import get_object_or_404


@unauthenticated_user
def loginUser(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            user = authenticate(request, username=data['username'], password=data['password'])
            # user2 = User.objects.get(username=data['username'])
            try:
                user2 = get_object_or_404(User, username=data['username'])
            except:
                messages.add_message(request, messages.ERROR, 'Username and Password invalid')
                return redirect('/login')

            if user is not None:
                if not user.is_staff and not user.is_superuser:
                    login(request, user)
                    return redirect('/welcome')

                elif user.is_staff and not user.is_superuser:
                    login(request, user)
                    return redirect('/welcome')

                elif user.is_staff and user.is_superuser:
                    login(request, user)
                    return redirect('/welcome')
            else:
                if not user2.is_active:
                    messages.add_message(request, messages.ERROR, 'Please Activate your Account')
                    return render(request, 'accounts/login.html',
                                  {'form': form, 'activeStatus': 'notActive', 'activateUserId': user2.id, 'activateUserUsername':user2.username, 'activateUserEmail':user2.email})

                else:
                    messages.add_message(request, messages.ERROR, 'Username and Password invalid')
                    return render(request, 'accounts/login.html', {'form': form})

    context = {
        'form': LoginForm
    }
    return render(request, 'accounts/login.html', context)

def welcomeUser(request):
    return HttpResponse('You are successfully logged in')

@unauthenticated_user
def registerUser(request):
    if request.method == 'POST':

        data = json.loads(request.POST.get('submit_registration_form'))
        print(data)

        username = data[1]['value']
        email = data[2]['value']
        password1 = data[3]['value']
        password2 = data[4]['value']
        print(username, email, password1, password2)

        if len(username) and len(email) and len(password1) and len(password2) > 0:
            if len(str(username)) > 6:

                if not re.search('\s', str(username)) and re.search("@", email):
                    if not User.objects.filter(username=username).exists() and not User.objects.filter(
                            email=email).exists():

                        if str(username).isalnum():
                            if password2 == password1:
                                user = User.objects.create_user(username=username, email=email, password=password2)
                                user.is_active = False
                                user.save()

                                otpValue = random.randint(100000, 999999)

                                sender_email = "tkintercms@gmail.com"
                                receiver_email = email
                                password = "Test@12345"

                                message = MIMEMultipart("alternative")
                                message["Subject"] = "Activate Account"
                                message["From"] = "info@test.com"
                                message["To"] = receiver_email

                                # Creating the plain-text and HTML version of your message
                                text = """\
                                Hi,
                                How are you?
                                entrance preparation has many great tutorials:
                                www.entancepreparation.com"""
                                html = """\
                                <html>
                                  <body>
                                    <h1>Hi, """ + username + """<br>
                                       <br>
                                    </h1>
                                    <h2>Please activate your account using OTP:</h2>
                                    <br>
                                    <h2 style="color:green;">""" + str(otpValue) + """</h2>
                                  </body>
                                </html>
                                """

                                # Turn these into plain/html MIMEText objects
                                part1 = MIMEText(text, "plain")
                                part2 = MIMEText(html, "html")

                                # Add HTML/plain-text parts to MIMEMultipart message
                                # The email client will try to render the last part first
                                message.attach(part1)
                                message.attach(part2)

                                # Create secure connection with server and send email
                                context = ssl.create_default_context()
                                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                                    server.login(sender_email, password)
                                    server.sendmail(
                                        sender_email, receiver_email, message.as_string()
                                    )

                                return JsonResponse({'status': True, 'otp': str(otpValue), 'userID': user.id})

                        return JsonResponse({'status': False})
                    return JsonResponse({'status': False})
                return JsonResponse({'status': False})

            return JsonResponse({'status': False})
        return JsonResponse({'status': False})

    context = {
        'form': UserRegisterForm
    }
    return render(request, 'accounts/register.html', context)


def activateUser(request):
    userID = json.loads(request.POST.get('userID'))
    print(userID)
    user = User.objects.get(pk=userID)
    user.is_active = True
    user.save()
    return JsonResponse({'status': True})


def activateUserLogin(request):
    userId = json.loads(request.POST.get('activateUserId'))
    data = User.objects.get(pk=userId)
    otpValue = random.randint(100000, 999999)

    # server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    #
    # server.login("tkintercms@gmail.com", "tkinter@12345")

    sender_email = "tkintercms@gmail.com"
    receiver_email = data.email
    password = "Test@12345"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Activate Account"
    message["From"] = "info@test.com"
    message["To"] = receiver_email

    # Creating the plain-text and HTML version of your message
    text = """\
                                    Hi,
                                    How are you?
                                    entrance preparation has many great tutorials:
                                    www.entancepreparation.com"""
    html = """\
                                    <html>
                                      <body>
                                        <h1>Hi, """ + data.username + """<br>
                                           <br>
                                        </h1>
                                        <h2>Please activate your account using OTP:</h2>
                                        <br>
                                        <h2 style="color:green;">""" + str(otpValue) + """</h2>
                                      </body>
                                    </html>
                                    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

    return JsonResponse({'status': True, 'otp': str(otpValue), 'userID': userId})


def logoutUser(request):
    logout(request)
    return redirect('/')


def registerUsernameValidation(request):
    if request.method == "POST":
        username = request.POST['username']
        if len(username) > 0:
            if len(str(username)) > 6:

                if not re.search('\s', str(username)):
                    if not User.objects.filter(username=username).exists():

                        if not str(username).isalnum():
                            return JsonResponse(
                                {'username_error': 'Username must contain alphabet, number and no blank space'})

                        else:
                            return JsonResponse({'username_valid': 'Username available'})

                    else:
                        return JsonResponse({'username_error': 'Username already taken'})
                else:
                    return JsonResponse({'username_error': 'Username can not contain space'})

            else:
                return JsonResponse({'username_error': 'Username must be greater than 6 character'})
        else:
            return JsonResponse({'username_error': 'Username cannot be empty'})


def registerEmailValidation(request):
    if request.method == "POST":
        email = request.POST['email']
        if len(email) > 0:
            if re.search("@", email):
                if not User.objects.filter(email=email):
                    return JsonResponse({"email_valid": "Email looks good"})
                else:
                    return JsonResponse({"email_error": "Email already exists"})
            else:
                return JsonResponse({"email_error": "Email Invalid"})
        else:
            return JsonResponse({"email_error": "Email can not be empty"})


def registerConfirmPassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        print(len(password), " password")
        if len(password) > 0 or len(confirmPassword) > 0:

            if len(confirmPassword) > 8 or len(password) > 8:

                if not re.search('\s', str(password)) or re.search('\s', str(confirmPassword)):

                    if not str(confirmPassword).isalnum() or not str(password).isalnum():

                        if password == confirmPassword:
                            return JsonResponse({'password_matched': 'Password Matched'})

                        elif str(confirmPassword).isdigit() or str(password).isdigit():
                            return JsonResponse({'password_unMatched': 'Your password can’t be entirely numeric'})

                        else:
                            return JsonResponse({'password_unMatched': 'Password Not Matched'})
                    else:
                        return JsonResponse(
                            {'password_unMatched': 'Password must contains alphabet, number, and Special characters'})

                else:
                    return JsonResponse({'password_unMatched': 'Password cannot contain space'})

            else:
                return JsonResponse({'password_unMatched': 'Password Must be greater than 8 character'})
        else:
            return JsonResponse({'password_unMatched': 'Password can not be Empty'})
