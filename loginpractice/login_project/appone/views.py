from django.shortcuts import render
from .forms import UserForm, userProfileInfoForm
from django.contrib.auth.hashers import make_password, check_password

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = userProfileInfoForm()
        print("user_info:", user_form)

        if user_form.is_valid():
            user = user_form.save()
            pwd_check(user.password)
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True

        else:
            print("Invalid FORM: ", user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile = userProfileInfoForm()
    return render(request, 'registration.html', context={'user_form': user_form, 'registered': registered})


def pwd_check(pwd):
    hashed_pwd = make_password(pwd)
    print(check_password(pwd, hashed_pwd))



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed USERNAME ", username, " password ", password)
    else:
        return render(request, 'login.html')
