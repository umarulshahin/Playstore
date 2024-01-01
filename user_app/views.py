from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse

# Create your views here.



def Login(request):
    return render(request,'user_auth/Login.html')

def Signup(request):
    return render(request,'user_auth/Signup.html')

def Signup_Otp(request):
    return render(request,'user_auth/Signup_otp.html')
    
def Forget_pass(request):
    return render(request,'user_auth/Forget_pass.html')

def New_pass(request):
    return render(request,'user_auth/New_pass.html')
def Forget_Otp(request):
    return render(request,'uera_auth/Forget_otp.html')