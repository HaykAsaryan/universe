import random
from urllib import response
from .models import Profile, Post
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
            response = redirect(f"/profile/{username}")
            response.set_cookie("current_user", username)
            return response
        else:
            messages.info(request, "Username or Password is incorrect.")

    context = {}

    return render(request, 'authorization.html', context)
    

def profilePage(request, username):
    user = User.objects.get(username = username)
    post = Post.objects.filter(username = username)
    context = {
        "post": post,
        "user": user
    }
    if request.method == "POST":
        if request.user:
            return render(request, "profile.html", request)
        else:
            return render(request, "login.html")
    return render(request, "profile.html", context)


@login_required
def logoutPage(request):
    logout(request)
    response = redirect("/authorization")
    response.delete_cookie("current_user")
    return response

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
        posts = request.POST.get("posts")
        image = request.FILES.get("image")
        old_user = Profile.objects.get(username = username)
        first_name = old_user.first_name if first_name == "" else first_name
        last_name = old_user.last_name if last_name == "" else last_name
        email = old_user.email if email == "" else email
        image = image

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
                profile.posts = posts

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
            profile.posts = posts
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

@login_required
def post(request, username):
    if request.method == "POST":
        image = request.FILES.get("image")
        text = request.POST.get("text")
        profile = Profile.objects.get(username=username)
        profile.posts = profile.posts + 1
        profile.save()
        Post.objects.create(
            profile_id=profile.id,
            image = image,
            text = text,
            username = username
        )
        return redirect(f"/profile/{username}")

@login_required
def like(request, username):
    if request.method == "POST":
        id = request.POST.get("id")
        likes_count = request.POST.get("likes_count").replace("💜", "")
        likes_count = likes_count.replace(" ", "")
        post = Post.objects.get(id = id)
        post.likes_count = int(likes_count) + 1
        post.save()
        if request.COOKIES.get("current_user"):
            return redirect(f"/profile/{username}")
        else:
            return redirect(f"/authorization")

def homePage(request):
    posts = list(Post.objects.all())
    random.shuffle(posts)
    context = {
        "posts": posts
    }
    if request.COOKIES.get("current_user"):
        current_user = request.COOKIES.get("current_user")
        user = Profile.objects.get(username = current_user)
        context["user"] = user
        context["exists"] = True
    return render(request, "home.html", context)

@login_required
def deletePage(request, username):
    user = User.objects.get(username = username)
    user.delete()
    return redirect(request, "delete.html")

@login_required
def deletePost(request, id):
    post = Post.objects.get(id = id)
    user = post.username
    if post:
        post.delete()
        return redirect(f"/profile/{user}")
    return render(request, "delete.html")


def custom_page_not_found_view(request, exception):
    response = render(request, "error.html", {
        "status": "404 - Not Found",
        "text": "Server cannot find the requested resource. Please, check site url."
    })
    response.status_code = 404
    return response

def custom_error_view(request):
    response = render(request, "error.html", {
        "status": "500 - Internal Server Error",
        "text": "Server encountered an unexpected condition that prevented it from fulfilling the request. Please, try again."
    })
    response.status_code = 500
    return response

def custom_permission_denied_view(request, exception):
    response = render(request, "error.html", {
        "status": "403 - Forbidden",
        "text": "Server understands the request, but refuzed to authorize it. Please, try again (re-authenticating makes no difference)."
    })
    response.status_code = 403
    return response

def custom_bad_request_view(request, exception):
    response = render(request, "error.html", {
        "status": "400 - Bad Request",
        "text": "Bad request. Please, try modificate the request and try again."
    })
    response.status_code = 400
    return response