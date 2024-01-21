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
    
    user = request.user
    if user:
        user_details = CustomUser.objects.get(id=id)
        
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
                     
                     
                      # .................ADDRESS AND ADD ADDRESS......................
                     
login_required(login_url='login')     
@never_cache                
def Addresses(request):
    
    
    user=CustomUser.objects.get(email=request.session.get("user_email"))
    value=User_Address.objects.filter(customuser=user.id)
    
    context={
        
        'value' : value
    }
    
    
    return render(request,'dashbord/address.html',context)


         # .................END ADDRESS AND ADD ADDRESS......................
         
          # ................. ADD ADDRESS......................
          
def Add_Address(request):
    
    user=CustomUser.objects.get(email=request.session.get("user_email"))
    
    if request.method == "POST":
    
            name=request.POST.get("name")
            email=request.POST.get("email")
            phone=request.POST.get("phone")
            house=request.POST.get("house")
            street=request.POST.get("street")
            city=request.POST.get("city")
            state=request.POST.get("state")
            country=request.POST.get("country")
            pin_code=request.POST.get("pin_code")
            location=request.POST.get("location")
            
            
            pattern = r'^[\w-]+$'
            pattern_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            pattern_Phone= r'^\d{3}-?\d{3}-?\d{4}$'
                
            if not (name or email or phone or house or street or city or country or pin_code or location):
                    messages.error(request, "please Fill Required Field")
                    return redirect("addresses")
                
            if not re.match(pattern,name and house and street and city or country and pin_code or location):
                    messages.error(request,"Please Enter Valid values")
                    return redirect("addresses") 
                
            elif not re.match(pattern_email,email):
                    messages.error(request,"Please enter valid email address")
                    return redirect("addresses")
                
                # elif CustomUser.objects.filter(email=email).exists():
                #     messages.error(request,"Email already exists")
                #     return render(request,'dashbord/profile.html')
                
            elif not re.match(pattern_Phone,phone):
                    messages.error(request,"Please enter valid Phone number")
                    return redirect("addresses")
                
            
            value=CustomUser.objects.get(id=user.id)
            
            
            User_Address.objects.create(
                name=name,
                email=email,
                phone=phone,
                house=house,
                street=street,
                city=city,
                state=state,
                country=country,
                pin_code=pin_code,
                location=location,
                customuser= value,
                                        
                                        
                                        )
       
       
            return redirect("addresses")
        
        
    return redirect("addresses")
    
           # .................END ADD ADDRESS......................
         
         # .................DELETE ADDRESS......................
         
def Delete_Address(request,id):
    
       if id:
           
           User_Address.objects.filter(id=id).delete()
           
           
           return redirect("addresses")
        
        
    
         
         # .................END DELETE ADDRESS......................
         
         # .................EDIT ADDRESS......................
         
def Edit_Address(request):
    
    if request.method == "POST" :
        
            E_name=request.POST.get("editName")
            E_email=request.POST.get("editEmail")
            E_phone=request.POST.get("editphone")
            E_house=request.POST.get("editHouse")
            E_street=request.POST.get("editStreet")
            E_city=request.POST.get("editcity")
            E_state=request.POST.get("editstate")
            E_country=request.POST.get("editcountry")
            E_pin_code=request.POST.get("editpin_code")
            E_location=request.POST.get("editlocation")
            address_id = request.POST.get('editid')
            
            pattern = r'^[\w-]+$'
            pattern_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            pattern_Phone= r'^\d{3}-?\d{3}-?\d{4}$'
                
            if not (E_name or E_email or E_phone or E_house or E_street or E_city or E_country or E_pin_code or E_location):
                    messages.error(request, "please Fill Required Field")
                    return redirect("addresses")
                
            if not re.match(pattern,E_name and E_house and E_street and E_city or E_country and E_pin_code or E_location):
                    messages.error(request,"Please Enter Valid values")
                    return redirect("addresses") 
                
            elif not re.match(pattern_email,E_email):
                    messages.error(request,"Please enter valid email address")
                    return redirect("addresses")
                
                # elif CustomUser.objects.filter(email=email).exists():
                #     messages.error(request,"Email already exists")
                #     return render(request,'dashbord/profile.html')
                
            elif not re.match(pattern_Phone,E_phone):
                    messages.error(request,"Please enter valid Phone number")
                    return redirect("addresses")
                
            
        
            User_Address.objects.filter(id=address_id).update(name=E_name,
                                                  email=E_email,
                                                  phone=E_phone,
                                                  house=E_house,
                                                  street=E_street,
                                                  city=E_city,
                                                  state=E_state,
                                                  country=E_country,
                                                  pin_code=E_pin_code,
                                                  location=E_location
                                                  )
        

    return redirect("addresses")
         
         # .................END EDIT ADDRESS......................

    
    