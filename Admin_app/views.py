from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from user_app.models import *
from .models import *


# Create your views here.


               # ........... Admin Authentication................

def Admin(request):
    
    if request.method == "POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        
        user=authenticate(email=email,password=password)
        
        if user is not None and user.is_superuser:
            login(request,user)
            return redirect("admin_dashbord")
        else:
            messages.error(request, "Email or Passwors mismatch")
            return render(request,"Admin/admin_login.html")

        
    return render(request,"Admin/admin_login.html")

              # ........... End Admin Authentication................
      
              # ............ Admin Dashbord ....................

def Admin_dashbord(request):
    
    return render(request,"Admin/admin_dashbord.html")

def Admin_logout(request):
    
    logout(request)
    
    return render(request,"Admin/admin_login.html")

                # ............ End Admin Dashbord ....................
                
                # ..............User List ..........................

def User_list(request):
    
    user=CustomUser.objects.filter(is_staff=False).values()
    print(user)
    
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
        print(sub,".....2")
        cate=request.POST.get("category_type")
        
        print(cate,"....1")
        id=Category.objects.get(id=cate)
        Sub_Category.objects.create(name=sub,category=id)
        
        return redirect("sub_category")
        
    
    
        
                    
                    
                    # ................End Add Sub Category .........................

    
    
    
    
