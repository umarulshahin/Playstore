from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


# Create your views here.

def Admin(request):
    if request.method == "POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        print(email,password,"......!")
        user=authenticate(email=email,password=password)
        print(user,"......111")
        if user is not None and user.is_superuser:
            print(".......2")
            login(request,user)
            return redirect("admin_dashbord")
        else:
            messages.error(request, "Email or Passwors mismatch")
            return render(request,"Admin/admin_login.html")

        
    return render(request,"Admin/admin_login.html")

def Admin_dashbord(request):
    
    return render(request,"Admin/admin_dashbord.html")

def Admin_logout(request):
    
    logout(request)
    
    return render(request,"Admin/admin_login.html")
def User_list(request):
    
    data=
    
    
    return render(request,"Admin/user_list.html")
    
    
