from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import *
from django.contrib import messages
import re 
import random
from twilio.rest import Client
import os
from dotenv import load_dotenv
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import  never_cache,cache_control
from django.contrib.auth.decorators import login_required 
from User_Home_app.models import *
from Admin_app.models import *
from django.contrib.auth.hashers import make_password, check_password
import string



 #    ............................USER AUTHENTICATION...........................
    #    ......................................................................
    
    

                 # ................. Login ................

@never_cache
def Login(request):
    
    try:
        if  'email_user' in request.session :
            return redirect("Dashbord")
        
        elif 'phone' in request.session:
            
            return redirect("signup_otp")
        
        
        if request.method == 'POST':
            email=request.POST.get("email")
            password=request.POST.get("password")
            user= authenticate(request,email=email,password=password)
            
            try :
                
                 status=CustomUser.objects.get(email=email)
            
            except Exception as e:
                
                messages.error(request, "Email or Passwors mismatch")
                return render(request,'User_auth/Login.html')
            
            if not status.is_active:
                
                messages.error(request, "Your account is Blocked")
                return render(request,'User_auth/Login.html')
            
            if user is not None  and not user.is_staff and user.is_active:
                
                
                request.session['user_email']=email
                login(request,user)
                return redirect("Dashbord")
                
            else: 
                messages.error(request, "Email or Passwors mismatch")
                return render(request,'User_auth/Login.html')
                

        return render(request,'User_auth/Login.html')   
    except Exception as e: 

        error=type(e).__name__
        typee,code=statuss_code(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'User_auth/auth_error.html',context)
    
               # ................. End Login ................
    
 
    
               # .................. Signup ..................
               
               
@never_cache
def Signup(request):
    
    try:
        if  'user_email' in request.session :
            return redirect("Dashbord")
        
        elif 'phone' in request.session:
            
            return redirect("signup_otp")    
        
        if request.method =="POST":
            
            username=request.POST.get("fname")
            L_name=request.POST.get("lname")
            email=request.POST.get("email")
            phone=request.POST.get("phone")
            password=request.POST.get("password")
            con_Password=request.POST.get("confirm_password")
            
            #  ..........  regx patterns ..........
            
            pattern = r'^[a-zA-Z0-9].*'
            pattern_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            pattern_Phone= r'^(?!0{10}$)\d{10}$'
            pattern_pass = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
            
            
            #  ..........  End regx patterns ..........
            
            
            # ........... Form Validation ............
            
            if not (username and L_name and email and phone and password and con_Password):
                messages.error(request, "please Fill Required Field")
                return render(request,'User_auth/Signup.html')
            
            if not re.match(pattern,username and L_name):
                messages.error(request,"Please Enter Valid User Name")
                return render(request,'User_auth/Signup.html')
            
            elif not re.match(pattern_email,email):
                messages.error(request,"Please enter valid email address")
                return render(request,'User_auth/Signup.html')
            
            elif CustomUser.objects.filter(email=email).exists():
                messages.error(request,"Email already exists")
                return render(request,'User_auth/Signup.html')
            
            elif not re.match(pattern_Phone,phone):
                messages.error(request,"Please enter valid Phone number")
                return render(request,'User_auth/Signup.html')
            
            elif CustomUser.objects.filter(ph_no=phone).exists():
                messages.error(request,"Phone number already exists")
                return render(request,'User_auth/Signup.html')
            
            elif not re.match(pattern_pass,password):
                messages.error(request,"The password is too weak")
                return render(request,'User_auth/Signup.html')
            
            elif password != con_Password:
                messages.error(request,"Password mismath")
                return render(request,'User_auth/Signup.html')
            

            
            
            # ...........End Form Validation ............

            
            
            try: 
                
                values=otp()
                
                
            except Exception as e:
            
                CustomUser.objects.filter(email=email).delete()
                messages.error(request,"OTP genaration failed")
            
                return redirect("signup")
            
            user_data = CustomUser.objects.create_user(email=email,password=password,username=username,ph_no=phone)
            user_data.save()
            
            request.session['otp']=values
            request.session['phone'] = phone
            
            
            return redirect("signup_otp")
        
        return render(request,'User_auth/Signup.html')
    
    except Exception as e: 

        error=type(e).__name__
        typee,code=statuss_code(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'User_auth/auth_error.html',context)



     # ......... End Signup .............
     

     # ........ Signup OTP Varification.......
     
@never_cache 
def Signup_Otp(request):
    try:
            
            otp=request.session.get("otp")
            re_otp=request.session.get("re_otp")
            user = CustomUser.objects.get(ph_no = request.session.get('phone'))
            if request.method =="POST":
                
                action = request.POST.get('action')
                if action == 'verify':
                    s_otp=request.POST.get("otp")
                    
                    if str(otp) == s_otp or str(re_otp) == s_otp:  
                        
                        #............ Referral Code Genarating...........
                        length = 8
                        characters = string.ascii_uppercase + string.digits
                        code=''.join(random.choice(characters) for _ in range(length))
                        
                        user.rafferal_code = code
                        user.save()
                        request.session.flush()
                        
                        messages.success(request,"Otp Verified..!")
                        return render(request,"User_auth/referral.html")
                    
                    else: 
                        messages.error(request,"Otp mismatch")
                        return render(request,'User_auth/Signup_otp.html')   
                        
                    
                elif action == 'cancel':
                    
                    request.session.flush()
                    user.delete()
                    return redirect('signup')
            return render(request,'User_auth/Signup_otp.html')
        
    except Exception as e: 
        error=type(e).__name__
        typee,code=statuss_code(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'User_auth/auth_error.html',context)


       # ........End  Signup OTP Varification .......
       
       
       # .................Logout ....................
       
@never_cache
def Logout(request):
    
    try:
        if 'user_email' in request.session:
            
            logout(request)
            request.session.flush()
            return redirect("Dashbord")
        else:
            logout(request)
            return redirect("Dashbord")
    except Exception as e: 

        error=type(e).__name__
        typee,code=statuss_code(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'User_auth/auth_error.html',context)
       # ..................End Logout ................
       
       
    #    ............................END USER AUTHENTICATION...........................
    #    ......................................................................


       
    #    ............................FORGET PASSWORD...........................
    #    ......................................................................
       
       # .....................Forget Password ...............
       
@never_cache      
def Forgot_pass(request):
    
    try:
        if request.method == "POST":
            action=request.POST.get("action")
            email=request.POST.get("email")
            
                    
            if action == "send OTP":
                
                try :
                    
                    email_f=CustomUser.objects.get(email=email)
                
                except Exception as e:
                    
                    messages.error(request,"Email not exist")
                    return redirect("forgot_pass")
            
                try:
                    
                    f_otp=otp()  
                
                    
                except Exception as e:
                
                    messages.error(request,"OTP genaration failed")
                    return redirect("forgot_pass")
                
                request.session['otp']=f_otp
                request.session['email'] =email_f.email
                return render(request,'User_auth/Forget_otp.html')
            
            else:
                
                return render (request,'User_auth/Login.html') 
        
            
        return render(request,'User_auth/Forget_pass.html')
    
    except Exception as e: 

        error=type(e).__name__
        typee,code=statuss_code(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'User_auth/auth_error.html',context)

        # ........End Forget Password .......
        
        
        # ........Forget OTP Check .......
        
@never_cache
def Forget_OTP_check(request):
    
    try:
    
        if request.method == "POST":
            
            f_otp=request.POST.get("otp") 
            action=request.POST.get("action")
            
            if action == "verify":
                
                f_re_otp=request.session.get("F_re_otp")
                otp=request.session.get("otp")
                
                print(f_re_otp,"...............weegds")
                
                if f_otp == str(otp) or  f_otp ==str(f_re_otp) :
                    
                    return redirect("new_pass")
                
                else:
                    messages.error(request,"OTP  Incurrct")
                    return redirect("forget_OTP_check") 
                
            else:
        
                return render (request,'User_auth/Login.html')
            
        return render (request,'User_auth/Forget_otp.html')
    except Exception as e: 

        error=type(e).__name__
        typee,code=statuss_code(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'User_auth/auth_error.html',context)

                
                
 
        # ........End Forget OTP Check .......
        
         # ........New Password .............
         
@never_cache       
def New_pass(request):
    
    try:
        if request.method == "POST" :
            password=request.POST.get("password")
            con_pass=request.POST.get("con_password")
            action=request.POST.get("action")
            pattern_pass = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
            
            if action == "save":
                
                if  not re.match(pattern_pass,password):
                    
                    messages.error(request,"The password is too weak")
                    return render(request,'User_auth/New_pass.html') 
                    
                if password != con_pass:
                    messages.error(request,"Password  mismatch")
                    return redirect("new_pass")  
                else: 
                    user=CustomUser.objects.get(email=request.session.get('email'))
                    
                    hashed_password = make_password(password)
                    user.password = hashed_password
                    user.save()
                    return redirect("login")

            else:
                return render (request,'User_auth/Login.html')
        return render(request,'User_auth/New_pass.html')
    except Exception as e: 

        error=type(e).__name__
        typee,code=statuss_code(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'User_auth/auth_error.html',context)
             
              # ........End New Password .............


 #    ............................ END FORGET PASSWORD...........................
    #    ......................................................................


   
       # ........ Block Check............
       
@never_cache
def Block_Check(request, id):
    
    try:
        try:
            
            email = request.session.get("user_email")

            user = get_object_or_404(CustomUser, id=id)
            

        
            if user.email == email:
                logout(request)
                del request.session['user_email']

        except CustomUser.DoesNotExist:
            return redirect("user_list")

        return redirect("user_list")
    except Exception as e: 

        error=type(e).__name__
        typee,code=statuss_code(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'User_auth/auth_error.html',context)


       
       # ........ End Block Check.......
       
    # ........ OTP Genarating ........
    
def otp():
    
        otp= random.randint(100000,999999)
        load_dotenv()
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        my_number = os.getenv('MY_NUMBER')
        print(otp,".............otp")
        client = Client(account_sid,auth_token)
        
        msg = client.messages.create(
            
            body = F"Your OTP is {otp}",
            from_= "+13395007651",
            to =my_number,
            
            
                                     )
        return otp
    
    # ........ End OTP Genarating ........
    
    # .............Signup Resend OTP ..........
    
@never_cache
def Signup_Resend_Otp(request):
    
    
    try:
    
        try: 
                
                re_otp=otp()
                
                
        except Exception as e:
            
            messages.error(request,"OTP genaration failed")
            return render(request,'User_auth/Signup_otp.html') 
        
        request.session["re_otp"]=re_otp
        return redirect('signup_otp') 
    
    except Exception as e: 

        error=type(e).__name__
        typee,code=statuss_code(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'User_auth/auth_error.html',context)


     # .............End Signup Resend OTP ..........
     
     # .............FORGOT Resend OTP ..........
     
@never_cache     
def Forgot_Resend_Otp(request):
    
    try:
        try: 
                
                re_otp=otp()
                
                
        except Exception as e:
            
            messages.error(request,"OTP genaration failed")
            return render(request,'User_auth/Signup_otp.html') 
        
        print(re_otp,"................426")
        request.session["F_re_otp"]=re_otp
        return redirect('forget_OTP_check') 
    except Exception as e: 

        error=type(e).__name__
        typee,code=statuss_code(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'User_auth/auth_error.html',context)

     # .............END FORGOT Resend OTP ..........

     # .............REFFERAL CODE CHEKING ..........


@never_cache   
def Referral(request):
    
    try:
        if request.method == "POST":
            
            action = request.POST.get("action")
            code = request.POST.get("code")
            
          
            
            if action == "verify":
                try:
                    
                 user = CustomUser.objects.get(rafferal_code = code)
                 
                except Exception as e:
                    
                    messages.error(request,"Referal Code Mismatch ")
                    return render(request,'User_auth/referral.html')
                
                if user :
                    
                    new_user = CustomUser.objects.get(ph_no = request.session.get('phone'))   
                    user.wallet_bal += 50
                    user.save()
                    Wallet_Transactions.objects.create( customuser =user,
                                                    amount = 50,
                                                    resons = "Referral Bonus",
                                                    add_or_pay = "add" 
                                                    )
                                
                    new_user.wallet_bal += 100
                    new_user.save()
                    Wallet_Transactions.objects.create( customuser =new_user,
                                                    amount = 100,
                                                    resons = "Referral Offer",
                                                    add_or_pay = "add")
                    
                    messages.success(request,"Successfully signup ")
                    return redirect("login")
                else:
                    
                    messages.error(request,"Referal Code Mismatch ")
                    return render(request,'User_auth/referral.html')
                
            else:
                
                messages.success(request,"Successfully signup ")
                return redirect("login")
            
        else:
            
            return render(request,'User_auth/referral.html')
        
    except Exception as e: 

        error=type(e).__name__
        typee,code=statuss_code(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'User_auth/auth_error.html',context)
        
        
             # .............END FORGOT Resend OTP ..........

    
#.......................... STATUS CODE CHEKING.................

never_cache
def statuss_code(error):
    

    
    if error == 'ValidationError':
        type='Page not Found'
        code=404
        return type,code
    
    elif error == 'TypeError':
        
        type='Bad Request'
        code=400
        return type,code
    
    else:
        
        type='Page not Found'
        code=404
        return type,code

 #..........................END STATUS CODE CHEKING.................
        
                
        
        