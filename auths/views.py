from django.shortcuts import render, redirect
from .forms import Login,Register
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse


# Create your views here.
def logins(request):
    forms = Login()
    next_url = request.GET.get('next', '')
    return render(request, 'login.html', {'form': forms, 'next': next_url})

def register(request):
    forms = Register()
    return render(request=request, template_name="register.html", context={"form":forms})


def Checklogin(request):
    if request.method == "POST":
        forms = Login(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data["UserName"]
            password = forms.cleaned_data["Password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Directly set the redirection URL to the payment page
                payment_url = reverse('payment')
                return HttpResponseRedirect(payment_url)
            else:
                messages.error(request, "Invalid username or password.")
                return render(request, 'login.html', {'form': forms})
        else:
            messages.error(request, "Invalid form submission.")
            return render(request, 'login.html', {'form': forms})
    else:
        forms = Login()
        return render(request, 'login.html', {'form': forms})

def CheckloginAjaxs(request, UserName, Password):
    user = authenticate(request, username=UserName, password=Password)
    if user is not None:
        login(request, user)
        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid credentials'}, status=401)
def registerAction(request):
    if request.method == "POST":
        forms = Register(request.POST)
        if forms.is_valid():
            users = User.objects.filter(username=forms.data["UserName"]).all()
            if users.exists():
                return HttpResponse("The user is already registered")
            else:
                us = User.objects.create_user(
                    username=forms.data["UserName"],
                    email=forms.data["UserName"],
                    password=forms.data["Password"]
                )
                us.first_name = forms.data["Name"]
                us.last_name = forms.data["Family"]
                us.save()
                return HttpResponseRedirect("logins")
        else:
            return HttpResponse("Invalid form")
    else:
        forms = Register()
        return render(request, 'register.html', {'form': forms})

def some_view(request):
    username = "exampleUser"
    password = "examplePass"
    url = reverse('CheckloginAjaxs', args=[username, password])
    return HttpResponseRedirect(url)
def CheckAuth(request):
     if request.user.is_authenticated:
         return HttpResponse("User has signed in")
     else:
         return HttpResponse("User has not signed in")

def LogOut(request):
    logout(request)
    return HttpResponseRedirect("/auths/")

"""def CheckloginAjaxs(request,UserName,Password):
        username=UserName
        password=Password
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect("اطلاعات معتبر است، خوش آمدید")
        else:
            return HttpResponse("حسابی با این مشخصات یافت نشد")
            """

