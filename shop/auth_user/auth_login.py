from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password

from shop.models import User


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            username = username.lower()
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                messages.add_message(
                    request, messages.INFO, "НЕПРАВИЛЬНОЕ ИМЯ ПОЛЬЗОВАТЕЛЯ ИЛИ ПАРОЛЬ"
                )
                return redirect("login")
        except Exception as e:
            print(e)

            messages.add_message(request, messages.INFO, "ОШИБКА!")
            return redirect("login")
    return render(request, "register_views/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            print(username, password)
            username = username.lower()
            print("-------------1-------------------")
            password = make_password(password)
            print("-------------2-------------------")
            user = User(username=username, password=password)
            print("-------------3-------------------")
            user.save()
            print("-------------4-------------------")
            return redirect("login")
        except Exception as e:
            print(e)
            messages.add_message(request, messages.INFO, "ОШИБКА!")
            return redirect("register")

    return render(request, "register_views/register.html")


def logoutPage(request):
    logout(request)
    return redirect("/")
