import random
from .models import Profile
from .forms import CreateRegistrationForm
from .functions import sendMail, createCode
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

def registrationPage(request):
    form = CreateRegistrationForm()
    if request.method == "POST":
        form = CreateRegistrationForm(request.POST)
        if form.is_valid():

            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            username = request.POST.get("username")
            email = request.POST.get("email")
            verification_code = createCode()

            form.save(commit = False)
            form.save()

            user = User.objects.get(username=username)

            Profile.objects.create(user_id=user.id, first_name=first_name, last_name=last_name, username=username, email=email, verification_code=verification_code, image=random.choice([
                '/profile_pics/default/profile1.jpg',
                '/profile_pics/default/profile2.jpg',
                '/profile_pics/default/profile3.jpg',
                '/profile_pics/default/profile4.jpg',
            ]))
            
            
            sendMail("Register info", f"Hi {first_name}. You have successfuly registered in 'Universe'. If it's not you, please inform us with sending email to universe.social.network@gmail.com.\n\nWith love, Universe team.", email)


    context = {'form': form}
    return render(request, 'registration.html', context)


def authorizationPage(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:


            login(request, user)
            return redirect(f"/profile/{username}")
        else:
            messages.info(request, "Username or Password is incorrect.")

    context = {}

    return render(request, 'authorization.html', context)
    

@login_required
def profilePage(request, username):
    user = User.objects.get(username = username)
    context = {"user": user}
    if request.method == "POST":
        if request.user:
            return render(request, "profile.html", request)
        else:
            return render(request, "login.html")
    return render(request, "profile.html", context)


@login_required
def logoutPage(request):
    logout(request)
    return redirect("/authorization")


def recoveryPage(request):

    if request.method == "POST":
            username = request.POST.get("username")
            try:
                if request.POST.get("code"):
                    username = request.POST.get("username")
                    profile = Profile.objects.get(username=username)
                    if request.POST.get("code") == profile.verification_code:
                        user = User.objects.get(username=username)
                        user.set_password(request.POST.get("new_pass"))
                        user.save()
                        return redirect("/authorization")
                else:
                    profile = Profile.objects.get(username=username)
                    newCode = createCode()

                    profile.verification_code = newCode
                    profile.save()
                    sendMail("Password Recovery", f"Hello {profile.first_name}. You are trying to change your password. Your verification code is {newCode}. If it's not you, please ignore it don't mind).\nWith love, 'Universe' team.", profile.email)
                    return render(request, "pass_recovery.html", {"username": username, "code": True})
                    

            except:
                return render(request, "pass_recovery.html", {"message": "User with that username does not exist."})
    
    return render(request, "pass_recovery.html")


@login_required
def settingsPage(request, username):

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        new_username = request.POST.get("username")
        email = request.POST.get("email")
        image = request.POST.get("image")
        old_user = Profile.objects.get(username = username)
        first_name = old_user.first_name if first_name == "" else first_name
        last_name = old_user.last_name if last_name == "" else last_name
        email = old_user.email if email == "" else email
        image = old_user.image if image == "" else f"/profile_pics/default/{image}"


        if new_username != "":
            new = User.objects.filter(username = new_username)
            if new.count():
                raise ValidationError("User With Given Username Already Exists")
            else:
                user = User.objects.get(username = username)
                profile = Profile.objects.get(username = username)
                user.username = new_username
                user.first_name = first_name
                user.last_name = last_name
                user.email = email

                profile.username = new_username
                profile.first_name = first_name
                profile.last_name = last_name
                profile.email = email
                profile.image = image

                user.save()
                profile.save()
                sendMail("Data Changing", f"Hello {new_username}, Your data was successfuly changed.", email)
                return redirect("/authorization")
        else:
            user = User.objects.get(username = username)
            profile = Profile.objects.get(username = username)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email

            
            profile.first_name = first_name
            profile.last_name = last_name
            profile.email = email
            profile.image = image
            user.save()
            profile.save()

            context = {
                "user": user
            }
            sendMail("Data Changing", f"Hello {username}, Your data was successfuly changed.", email)
            return redirect("/authorization")

    
    user = User.objects.get(username = username)
    context = {"user": user}
    return render(request, "settings.html", context)
