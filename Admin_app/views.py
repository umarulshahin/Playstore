from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from user_app.models import *
from .models import *
from .views import *
from django.views.decorators.cache import  never_cache,cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
# from django.http import JsonResponse
# Create your views here.

          # ........... User Priventing Authentication................

def admin_required(view_func):
   
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url='admin_login'
    )

    return actual_decorator(view_func)
             
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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="admin_login")
@never_cache
def Admin_dashbord(request):
    
    
    return render(request,"Admin/admin_dashbord.html")

               # ............ End Admin Dashbord ....................
               
               
               # ............  Admin Logout ....................


def Admin_logout(request):
    
    if 'email_admin' in request.session:
        email_admin_value = request.session.get('email_admin')
        del request.session['email_admin']
       
        logout(request)
        return redirect("admin_login")

                # ............End Admin Logout  ....................
                
                # ..............User List ..........................
                
@admin_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="admin_login")
@never_cache
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
    return redirect("block_check",id=id)
    
        

                  # ................End User Block .........................
                  
                  # ................User UnBlock .........................
                  
def User_unblock(request,id):
    
    user=CustomUser.objects.get(id=id)
    user.is_active=True
    user.save()
    return redirect("user_list")

                # ................End User UnBlock ......................... 
                

                # ................Product Category......................... 
                
@admin_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="admin_login")
@never_cache
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
        
        if Category.objects.filter(name=name).exists():
            
            messages.error(request, "This Category Alredy Exist")
            return redirect("category_list")
        
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
                 
@admin_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="admin_login")
@never_cache    
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
        
        if  Sub_Category.objects.filter(name=name).exists():
            
            messages.error(request, " Sub Category Alredy Exist")
            return redirect("sub_category")
        
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
            
            messages.error(request, " Sub Category Alredy Exist")
            return redirect("sub_category")
        
        id=Category.objects.get(id=cate)
        Sub_Category.objects.create(name=sub,category=id)
        
        return redirect("sub_category")
        
                    
                    # ................End Add Sub Category .........................
                    
                    # ................Product .........................
@admin_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="admin_login")
@never_cache    
def Product_list(request):
    
    pro=Product.objects.all()
    sub=Sub_Category.objects.all()
    img=Product_image.objects.all().prefetch_related("product_set")
    
    
    context={
        'pro' : pro,
        'sub' : sub,
        'img': img
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
        m_image=request.FILES.get("m_image")
        r_images=request.FILES.getlist("r_images")
        
        
        if int(price) < 1:
            
             messages.error(request, "Invalid Price . Price Should Be Above Zero ")
             return redirect("product_list")
         
        if int(discount) < 0:
            
             messages.error(request, "Invalid Discound . Discound Should Be Zero or  Above Zero ")
             return redirect("product_list")
        
        sub=Sub_Category.objects.get(id=sub_category)
        pro_id=Product.objects.create(name=name,price=price,discount=discount,stock=stock,sub_category=sub,description=description,image=m_image)
 
    
        for i in range(len(r_images)):
            
            Product_image.objects.create(product=pro_id,image_url=r_images[i])
            
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
        r_image=request.FILES.getlist("related_images")
        delete=request.POST.getlist("selected_images")
        
      
       
        

     
        if int(price) < 1:
            
             messages.error(request, "Invalid Price . Price Should Be Above Zero ")
             return redirect("product_list")
         
        if discount < 0:
            
             messages.error(request, "Invalid Discound . Discound Should Be Zero or Above Zero ")
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
        
        if delete and r_image:
            for i in delete:
                
                Product_image.objects.filter(id=int(i)).delete()
                
            for j in r_image:
                
                Product_image.objects.create(product=up,image_url=j)
        elif delete:
            
             for i in delete:
                
                Product_image.objects.filter(id=int(i)).delete()
                
        elif r_image:
            
              for i in r_image:
            
                Product_image.objects.create(product=up,image_url=i)
            
           
        
    
    return redirect("product_list")
                    
                    # ................End Update Product .........................
                    
                    # ................ADD SIZE .........................
            
def Add_Size(request,id):
    
    if request.method == "POST":
        
        size=request.POST.get("size")
        stock=request.POST.get("stock")
        
       
        if int(size) <= 0 or int(stock) <= 0 :
                
                messages.error(request, "Invalid Size or Stock .Size and Stock Should Be Above Zero ")
                return redirect("product_list")
            
        else:
               
            value=Product.objects.get(id=id)
            
            Product_size.objects.create(size=size,stock=stock,product=value)
        
    return redirect("product_list")

                    # ................END ADD SIZE .........................
                    
#                     # ................EDIT SIZE .........................
def Edit_Size(request,id):
    
    if request.method == 'POST':
        
        for size_obj in Product_size.objects.filter(product_id=id):
            
            size = request.POST.get('size' + str(size_obj.id))
            stock = request.POST.get('stock' + str(size_obj.id))
            
            if int(size) <= 0 or int(stock) <= 0 :
                
                messages.error(request, "Invalid Size or Stock .Size and Stock Should Be Above Zero ")
                return redirect("product_list")
            
            else:
                size_obj.stock=stock 
                size_obj.size=size 
                size_obj.save()

        
    return redirect("product_list")

                    
                    # ................END EDIT SIZE .........................
    

# def your_ajax_view(request):
#     pro_id = request.GET.get('pro_id')
#     selected_size = request.GET.get('selected_size')

#     # Add your logic to get the stock based on the pro_id and selected_size
#     # For example, assuming Product has a method get_stock_for_size(selected_size)
#     product = Product.objects.get(id=pro_id)
#     stock = product.get_stock_for_size(selected_size)

#     # Return the stock in a JSON response
#     return JsonResponse({'stock': stock})
    
    
    
