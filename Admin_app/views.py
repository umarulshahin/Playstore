from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from user_app.models import *
from .models import *
from django.views.decorators.cache import  never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

          # ........... User Priventing Authentication................
          
def admin_required(Admin_dashbord):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url='admin_login'  
    )
    return actual_decorator(Admin_dashbord)
             
              # ...........End  User Priventing Authentication................


               # ........... Admin Authentication................
@never_cache
def Admin(request):
    
    if 'email_admin' in request.session:
        
        return redirect("admin_dashbord")
    
    if request.method == "POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        
        users=authenticate(email=email,password=password)
        
        if users is not None and users.is_staff:
            login(request,users)
            request.session['email_admin']=email
            return redirect("admin_dashbord")
        else:
            messages.error(request, "Email or Passwors mismatch")
            return render(request,"Admin/admin_login.html")

        
    return render(request,"Admin/admin_login.html")

              # ........... End Admin Authentication................
              
      
              # ............ Admin Dashbord ....................
              
              
@admin_required
@login_required(login_url="admin_login")
@never_cache
def Admin_dashbord(request):
    
    
    return render(request,"Admin/admin_dashbord.html")

               # ............ End Admin Dashbord ....................
               
               
               # ............  Admin Logout ....................


@never_cache
def Admin_logout(request):
    
    if 'email_admin' in request.session:
        email_admin_value = request.session.get('email_admin')
        print(email_admin_value)
        del request.session['email_admin']
       
        logout(request)
        return redirect("admin_login")

                # ............End Admin Logout  ....................
                
                # ..............User List ..........................

def User_list(request):
    
    user=CustomUser.objects.filter(is_staff=False).values()
   
    
    context={
        
        "user":user
    }
    
    return render(request,"Admin/user_list.html",context)

                # ..............End User List ..........................
                
                # ................User Block .........................

def User_block(request,id):
    
    user=CustomUser.objects.get(id=id)
    user.is_active=False
    user.save()
    return redirect("user_list")

                  # ................End User Block .........................
                  
                  # ................User UnBlock .........................
                  
def User_unblock(request,id):
    
    user=CustomUser.objects.get(id=id)
    user.is_active=True
    user.save()
    return redirect("user_list")

                # ................End User UnBlock ......................... 
                
                # ................Product Category......................... 
                
def Category_list(request): 
    
    cate = Category.objects.all()
    
    context = {
        'cate' : cate
    }
    
    return render(request,'admin/Category.html',context)
                
                # ................End Product Category......................... 
                
                # ................Change Status.........................
                
def Change_Status(request,id):
    
    
    cate=Category.objects.get(id=id)
    
    
    if not cate.is_deleted :
        
        cate.is_deleted = True
        cate.save()
        
        
    else:
        
        cate.is_deleted = False
        cate.save()

    return redirect('category_list')
    
                
                # ................End Change Status.........................
                
                # ................Delete Change Category.......................
                
def Delete_category(request,id):
    
    cate = Category.objects.get(id=id)
    cate.delete()
    
    return redirect("category_list")
    
    
                # ................End Delete Change Category...............
                
                # ................ Update Category.........................
                
def Update_category(request,id):
    
    if request.method == 'POST':
        name=request.POST.get("category_name")
        Category.objects.filter(id=id).update(name=name)
    
    return redirect("category_list")
    
                
                # ................End  Update Category.................
                
                # ................Add Category.........................
                
def Add_category(request):
    
    if request.method == 'POST':
        name=request.POST.get("category_name")
        
        if  Category.objects.filter(name=name).exists():
            
            messages.error(request, "This Category Alredy Exist")
            return redirect("category_list")
            
            
        
        
        Category.objects.create(name=name)
        
        return redirect("category_list")
        
    
                # ................End  Add Category.........................
                
                 # ................Sub Category.........................
                 
def Sub_category(request):
    
    sub=Sub_Category.objects.all()
    main = Category.objects.all()
    
    
    context={
        'sub':sub,
        'main':main
    }

    return render(request,"admin/sub_category.html",context)
                 
                  # ................End sub Category.........................
                  
                  # ................Sub Category Status Change.........................
                  
def Status_Change(request,id):
    status=Sub_Category.objects.get(id=id)
    
    if not status.is_deleted:
        
        status.is_deleted=True
        status.save()
    else:
        
        status.is_deleted = False
        status.save()
        
    return redirect("sub_category") 
    
    
                  # ................Sub Category Status Change.........................
                  
                   # ................Sub Update Category .........................
                   
def Update_Sub_Category(request,id):
    
    if request.method == 'POST':
        
        name=request.POST.get("category_name")
        Sub_Category.objects.filter(id=id).update(name=name)
        
        return redirect("sub_category") 
    
                   
                    # ................End Update Sub Category .........................
                    
                    # ................Delete Sub Category .........................
                    
def Delete_Sub_Category(request,id):
    
    sub=Sub_Category.objects.get(id=id)
    sub.delete()
    
    return redirect("sub_category")
    
    
                    
                    # ................Delete Sub Category .........................
                    
                    # ................Add Sub Category .........................

def Add_Sub_Category(request):
    
    if request.method == 'POST' :
        sub=request.POST.get("category_name")
        cate=request.POST.get("category_type")
        if  Sub_Category.objects.filter(name=sub).exists():
            
            messages.error(request, "This Sub Category Alredy Exist")
            return redirect("sub_category")
        
        id=Category.objects.get(id=cate)
        Sub_Category.objects.create(name=sub,category=id)
        
        return redirect("sub_category")
        
                    
                    # ................End Add Sub Category .........................
                    
                    # ................Product .........................
                    
def Product_list(request):
    
    pro=Product.objects.all()
    sub=Sub_Category.objects.all()
    
    context={
        'pro' : pro,
        'sub' : sub
    }
    
    return render(request,"admin/Product.html",context)
                    
                    
                    # ................End Product .........................
                    
                    # ................ Product Status.........................
                    
def Product_Status(request,id):
   
    status=Product.objects.get(id=id)
    
    if not status.is_deleted:
        
        status.is_deleted = True
        status.save()
        
    else:
        
        status.is_deleted = False
        status.save()
        
    return redirect("product_list")
                    
                    # ................End Product Status.........................
                    
                    # ................Add Product .........................
                    
def Add_Product(request):
    
    if request.method == "POST" :
        
        name=request.POST.get("product_name")
        price=request.POST.get("price")
        discount=request.POST.get("discount")
        stock=request.POST.get("stock")
        sub_category=request.POST.get("category_type")
        description=request.POST.get("description")
        image=request.FILES.get("image")
        
        sub=Sub_Category.objects.get(id=sub_category)
        Product.objects.create(name=name,price=price,discount=discount,stock=stock,sub_category=sub,description=description,image=image)
        
        return redirect("product_list") 
        
    
                    
                    # ................End Add Product .........................
                    
                    
                    # ................Delete Product .........................
                    
def Delete_Product(request,id):
   
    pro=Product.objects.get(id=id)
    pro.delete()
    
    return redirect("product_list")
                    
                    
                    # ................End Delete Product .........................
                    
                    # ................Update Product .........................
                    
def Update_Product(request,id):
    
    if request.method == "POST" :
        up= Product.objects.get(id=id)
        name=request.POST.get("product_name")
        price=request.POST.get("price")
        discount=float(request.POST.get("discount"))
        stock=request.POST.get("stock")
        sub_category=request.POST.get("category_type")
        description=request.POST.get("description")
        image=request.FILES.get("image")
        print(type(discount))
        if int(price) < 1:
            
             messages.error(request, "Invalid Price . Price Should Be Above Zero ")
             return redirect("product_list")
        if discount < 1:
            
             messages.error(request, "Invalid Discound . Discound Should Be Above Zero ")
             return redirect("product_list")
         
            
    
        sub=Sub_Category.objects.get(id=sub_category)
        
        up.name=name
        up.price=price
        up.discount=discount
        up.stock=stock
        up.description=description
        up.sub_category=sub
        
        if image:
            up.image=image
            
        up.save()
    
    return redirect("product_list")
                    
                    # ................End Update Product .........................

    
    
    
    
