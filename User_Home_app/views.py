from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.cache import  never_cache,cache_control
from django.contrib.auth.decorators import login_required
from Admin_app.models import *
from user_app.models import *
from django.shortcuts import get_object_or_404
from django.contrib import messages
import re 

# Create your views here.

             # ................. Dashbord......................
@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Dashbord(request):
    
    pro=Product.objects.all()
    sub = Sub_Category.objects.filter(name="Nike").prefetch_related("product_set")
    
    context={
            'pro' : pro,
            'sub' : sub
        }
    
    return render(request,'dashbord/dashbord.html',context)

               # .................End Dashbord......................


               # ................. All Product......................
               
def All_Product(request):
    
    pro=Product.objects.all()
    
    context={
        'pro' : pro
    }
    
    return render(request,'dashbord/all_product.html',context)
    



               # ................. End All Product......................
               
               # ................. View Product......................
def View_Product(request,id):
    
    pro=get_object_or_404(Product,id=id)
    
    relate=Product.objects.exclude(id=id)[:4]
    
    context={
        
        'pro' : pro,
        'relate' : relate,
       
    }
    
    return render(request,'dashbord/view_product.html',context)
               
               # ................. End View Product......................
               
                  # ................. USER PROFILE......................

login_required(login_url='login')
def User_Profile(request,id):
    print(request.user.is_authenticated)
    user = request.user
    if user:
        user_details = CustomUser.objects.get(id=id)
        print(user_details)
        context = {
            'user' : user_details,
        }
        return render(request,'dashbord/profile.html',context)
    
    return redirect("login")
                  
                     # .................END USER PROFILE......................
                     
                     # .................EDIT PROFILE......................
                     
def Edit_Profile(request,id):
    
    if request.method == "POST":
        
        username=request.POST.get("editFirstName")
        email=request.POST.get("editEmail")
        phone=request.POST.get("editphone")
        
        pattern = r'^[\w-]+$'
        pattern_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        pattern_Phone= r'^\d{3}-?\d{3}-?\d{4}$'
        
        if not (username or email or phone ):
            messages.error(request, "please Fill Required Field")
            return render(request,'dashbord/profile.html')
        
        if not re.match(pattern,username):
            messages.error(request,"Please Enter Valid User Name")
            return render(request,'dashbord/profile.html')
        
        elif not re.match(pattern_email,email):
            messages.error(request,"Please enter valid email address")
            return render(request,'dashbord/profile.html')
        
        # elif CustomUser.objects.filter(email=email).exists():
        #     messages.error(request,"Email already exists")
        #     return render(request,'dashbord/profile.html')
        
        elif not re.match(pattern_Phone,phone):
            messages.error(request,"Please enter valid Phone number")
            return render(request,'dashbord/profile.html')
        
        # elif CustomUser.objects.filter(ph_no=phone).exists():
        #     messages.error(request,"Phone number already exists")
        #     return render(request,'dashbord/profile.html')
        
        
        
        CustomUser.objects.filter(id=id).update(username=username,email=email,ph_no=phone)
        
        
        
        
        return render(request,'dashbord/profile.html')
                     # .................END EDIT PROFILE......................
    