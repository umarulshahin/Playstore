from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.cache import  never_cache
from django.contrib.auth.decorators import login_required
from Admin_app.models import *

# Create your views here.

             # ................. Dashbord......................
@never_cache
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
    
    pro=Product.objects.filter(id=id)
    relate=Product.objects.exclude(id=id)[:4]
    context={
        'pro' : pro,
        'relate' : relate
    }
    
    return render(request,'dashbord/view_product.html',context)
               
               # ................. End View Product......................
    