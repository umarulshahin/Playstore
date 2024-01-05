from django.shortcuts import render,HttpResponse,redirect
from .models import *
from django.contrib import messages
import re 
import random
from twilio.rest import Client
import os
from dotenv import load_dotenv
from django.contrib.auth import authenticate,login,logout


 

# Create your views here.



def Login(request):
    
    
    if request.method == 'POST':
        email=request.POST.get("email")
        password=request.POST.get("password")
        print(password)
        user= authenticate(request,email=email,password=password)
        
        if user is not None and user.is_active:
            login(request,user)
            return redirect("Dashbord")
        else:  
            messages.error(request, "Email or Passwors mismatch")
            return render(request,'user_auth/Login.html')
            

    return render(request,'user_auth/Login.html')
    
    # ........ OTP Genarating ........

def otp():
        otp= random.randint(100000,999999)
        load_dotenv()
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        my_number = os.getenv('MY_NUMBER')
        
        client = Client(account_sid,auth_token)
        
        msg = client.messages.create(
            
            body = F"Your OTP is {otp}",
            from_= "+13346030540",
            to =my_number,
            
            
                                     )
        return otp
    
    # ........ End OTP Genarating ........
    
    # ......... Signup .........

def Signup(request):
    
    if request.method =="POST":
        
        username=request.POST.get("fname")
        L_name=request.POST.get("lname")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        password=request.POST.get("password")
        con_Password=request.POST.get("confirm_password")
        
        #  ..........  regx patterns ..........
         
        pattern = r'^[\w-]+$'
        pattern_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        pattern_Phone= r'^\d{3}-?\d{3}-?\d{4}$'
        pattern_pass = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
        
        
        #  ..........  End regx patterns ..........
        
        
        # ........... Form Validation ............
        
        if not (username or L_name or email or phone or password or con_Password):
            messages.error(request, "please Fill Required Field")
            return render(request,'user_auth/Signup.html')
        
        if not re.match(pattern,username and L_name):
            messages.error(request,"Please Enter Valid User Name")
            return render(request,'user_auth/Signup.html')
        
        elif not re.match(pattern_email,email):
            messages.error(request,"Please enter valid email address")
            return render(request,'user_auth/Signup.html')
        
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request,"Email already exists")
            return render(request,'user_auth/Signup.html')
        
        elif not re.match(pattern_Phone,phone):
            messages.error(request,"Please enter valid Phone number")
            return render(request,'user_auth/Signup.html')
        
        elif CustomUser.objects.filter(ph_no=phone).exists():
            messages.error(request,"Phone number already exists")
            return render(request,'user_auth/Signup.html')
        
        elif not re.match(pattern_pass,password):
            messages.error(request,"The password is too weak")
            return render(request,'user_auth/Signup.html')
        
        elif password != con_Password:
            messages.error(request,"Password mismath")
            return render(request,'user_auth/Signup.html')
        
        user_data = CustomUser.objects.create_user(email=email,password=password,full_name=username,ph_no=phone)
        user_data.save()
        
        # ...........End Form Validation ............

        
        
        try: 
            
            values=otp()
            print(values,"...........1")
            
        except Exception as e:
            print(".........2")
            CustomUser.objects.filter(email=email).delete()
            messages.error(request,"{e}")
            print(f"Error : {e}")
            return redirect("signup")
        
        request.session['otp']=values
        request.session['email'] = email
        
        return redirect("signup_otp")
    
    return render(request,'user_auth/Signup.html')

     # ......... End Signup .............
     

     # ........ Signup OTP Varification.......
     
def Signup_Otp(request):
    
    otp=request.session.get("otp")
    user = CustomUser.objects.get(email = request.session.get('email'))
    
    if request.method =="POST":
        action = request.POST.get('action')
        
        if action == 'verify':
            s_otp=request.POST.get("otp")
            
            if str(otp) != s_otp :  
                messages.error(request,"Otp mismatch")
                return render(request,'user_auth/Signup_otp.html')   
            else: 
                return redirect("login")
            
        elif action == 'cancel':
            user.delete()
            return redirect('signup')
           
    return render(request,'user_auth/Signup_otp.html')

       # ........End  Signup OTP Varification .......
       
       
def Logout(request):
   
    logout(request)
    return redirect("Dashbord")
       
    
def Forget_pass(request):
    return render(request,'user_auth/Forget_pass.html')

def New_pass(request):
    return render(request,'user_auth/New_pass.html')
def Forget_Otp(request):
    return render(request,'uera_auth/Forget_otp.html')