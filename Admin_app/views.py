from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from user_app.models import *
from .models import *
from User_Home_app.models import *
from django.db.models import Q
from .views import *
from django.views.decorators.cache import  never_cache,cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.db.models import *
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors     
from django.db.models.functions import Coalesce
import re 
from datetime import datetime



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
    try :
        
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
    
    except TypeError:
        return render(request,'Admin/admin_404.html')
    
              # ........... End Admin Authentication................
              
      
              # ............ Admin Dashbord ....................
              
              
@admin_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/Admin_app/")
@never_cache
def Admin_dashbord(request):
    
    try:
    
        if request.method =="POST":
            
            start_date=request.POST.get("startDate")
            end_date=request.POST.get("endDate")
            
            if start_date and end_date:
            
                total_sale=Order.objects.filter(status__in=['pending','processing','shipped','delivered'], created_date__range=(start_date, end_date)).aggregate(total=Coalesce(Sum('total_amount'), Value(0)))
                all_amount=Order.objects.filter(created_date__range=(start_date, end_date)).aggregate(total=Coalesce(Sum('total_amount'), Value(0)))
                
                total_sale=total_sale['total']//1000
                all_amount=all_amount['total']//1000
                
                cod_total=Order.objects.filter(payment_type="cashOnDelivery", created_date__range=(start_date, end_date),status__in=['pending','processing','shipped','delivered']).aggregate(total=Sum('total_amount'))
                upi_total=Order.objects.filter(payment_type="paid by Razorpay",created_date__range=(start_date, end_date),status__in=['pending','processing','shipped','delivered']).aggregate(total=Sum('total_amount'))
                
                pending=Order.objects.filter(status='pending',created_date__range=(start_date, end_date)).aggregate(total=Count("status"))
                processing=Order.objects.filter(status='processing',created_date__range=(start_date, end_date)).aggregate(total=Count("status"))
                shipped=Order.objects.filter(status='shipped',created_date__range=(start_date, end_date)).aggregate(total=Count("status"))
                delivered=Order.objects.filter(status='delivered',created_date__range=(start_date, end_date)).aggregate(total=Count("status"))
                cancelled=Order.objects.filter(status='cancelled',created_date__range=(start_date, end_date)).aggregate(total=Count("status"))
                refund=Order.objects.filter(status='refunded',created_date__range=(start_date, end_date)).aggregate(total=Count("status"))
                    
                adidas = Order_Items.objects.filter(order__created_date__range=(start_date,end_date),Sub_Category="2").aggregate(total=Sum('qty'))              
                puma= Order_Items.objects.filter(order__created_date__range=(start_date,end_date),Sub_Category="1").aggregate(total=Sum('qty'))
                nike= Order_Items.objects.filter(order__created_date__range=(start_date,end_date),Sub_Category="3").aggregate(total=Sum('qty'))
                
                all=Order.objects.filter(created_date__range=(start_date, end_date)).aggregate(total=Count('id'))
                
                context={
                        'total_sale' : total_sale,
                        'all_amount' : all_amount,
                        'cod_total'  : cod_total['total'],
                        'upi_total'  : upi_total['total'],
                        'pending'    : pending['total'],
                        'procrssing' : processing['total'],
                        'sipped'     : shipped['total'],
                        'delivered'  : delivered['total'],
                        'cancelled'  : cancelled['total'],
                        'refund'     : refund['total'],
                        'puma'       : puma['total'],
                        'adidas'     : adidas['total'],
                        'nike'       : nike['total'],
                        'all_category': all['total'],
                        
                    
                    }
                    
                    
                return render(request,"Admin/admin_dashbord.html",context)
            return render(request,"Admin/admin_dashbord.html")
        
            
        
        else:
                total_sale=Order.objects.exclude(Q(status="cancelled") &~ Q(status="refunded")).aggregate(total=Coalesce(Sum('total_amount'), Value(0)))
                all_amount=Order.objects.aggregate(total=Coalesce(Sum('total_amount'), Value(0)))
                
                total_sale=total_sale['total']//1000
                all_amount=all_amount['total']//1000
                
                
                cod_total=Order.objects.filter(payment_type="cashOnDelivery").aggregate(total=Sum('total_amount'))
                upi_total=Order.objects.filter(payment_type="paid by Razorpay").aggregate(total=Sum('total_amount'))
                
                pending=Order.objects.filter(status='pending').aggregate(total=Count("status"))
                processing=Order.objects.filter(status='processing').aggregate(total=Count("status"))
                shipped=Order.objects.filter(status='shipped').aggregate(total=Count("status"))
                delivered=Order.objects.filter(status='delivered').aggregate(total=Count("status"))
                cancelled=Order.objects.filter(status='cancelled').aggregate(total=Count("status"))
                refund=Order.objects.filter(status='refunded').aggregate(total=Count("status"))
                
                
                adidas=Order_Items.objects.filter(Sub_Category="2").aggregate(total=Sum('qty'))
                puma=Order_Items.objects.filter(Sub_Category="1").aggregate(total=Sum('qty'))   
                nike=Order_Items.objects.filter(Sub_Category="3").aggregate(total=Sum('qty'))
                all=Order.objects.all().aggregate(total=Count('id'))
                
            
                context={
                    'total_sale' : total_sale,
                    'all_amount' : all_amount,
                    'cod_total'  : cod_total['total'],
                    'upi_total'  : upi_total['total'],
                    'pending'    : pending['total'],
                    'procrssing' : processing['total'],
                    'sipped'     : shipped['total'],
                    'delivered'  : delivered['total'],
                    'cancelled'  : cancelled['total'],
                    'refund'     : refund['total'],
                    'puma'       : puma['total'],
                    'adidas'     : adidas['total'],
                    'nike'       : nike['total'],
                    'all_category': all['total'],
                }
                
                
                return render(request,"Admin/admin_dashbord.html",context)
            
    except TypeError:
         return render(request,'Admin/admin_404.html')

               # ............ End Admin Dashbord ....................
               
               
               # ............  Admin Logout ....................


def Admin_logout(request):
    
    try:
    
        if 'email_admin' in request.session:
          
            del request.session['email_admin']
            logout(request)
            
            return redirect("admin_login")
    except TypeError:
        return render(request,'Admin/admin_404.html')

                # ............End Admin Logout  ....................
                
                # ..............User List ..........................
                
@admin_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/Admin_app/")
@never_cache
def User_list(request):
    
    try:
        
        user=CustomUser.objects.filter(is_staff=False).values()
        
        context={
            
            "user":user
        }
        
        return render(request,"Admin/user_list.html",context)
    except TypeError:
        return render(request,'Admin/admin_404.html')

                # ..............End User List ..........................
                
                # ................User Block .........................
                
@admin_required
@login_required(login_url="/Admin_app/")
@never_cache
def User_block(request,id):
    
    try:
        
        user=CustomUser.objects.get(id=id)
        user.is_active=False
        user.save()
        return redirect("block_check",id=id)
    
    except TypeError:
        return render(request,'Admin/admin_404.html')


                  # ................End User Block .........................
                  
                  # ................User UnBlock .........................
@admin_required
@login_required(login_url="/Admin_app/")
@never_cache                 
def User_unblock(request,id):
    try:
        user=CustomUser.objects.get(id=id)
        user.is_active=True
        user.save()
        return redirect("user_list")
    except TypeError:
        return render(request,'Admin/admin_404.html')

                # ................End User UnBlock ......................... 
                

                # ................Product Category......................... 
                
@admin_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/Admin_app/")
@never_cache
def Category_list(request): 
    
    try:
        cate = Category.objects.all()
        
        context = {
            'cate' : cate
        }
        
        return render(request,'admin/Category.html',context)
    
    except TypeError:
        return render(request,'Admin/admin_404.html')
                
                # ................End Product Category......................... 
                
                # ................Change Status.........................
@admin_required
@login_required(login_url="/Admin_app/")
@never_cache               
def Change_Status(request,id):
    
    try: 
        cate=Category.objects.get(id=id)
        
        if not cate.is_deleted :
            
            cate.is_deleted = True
            cate.save()
            
        else:
            
            cate.is_deleted = False
            cate.save()

        return redirect('category_list')
    
    except TypeError:
        return render(request,'Admin/admin_404.html')
    
                
                # ................End Change Status.........................
                
                # ................Delete Change Category.......................
                
@admin_required
@login_required(login_url="/Admin_app/")
@never_cache                
def Delete_category(request,id):
    
    try:
        cate = Category.objects.get(id=id)
        cate.delete()
        
        return redirect("category_list")
    
    except TypeError:
        return render(request,'Admin/admin_404.html')
    
    
                # ................End Delete Change Category...............
                
                # ................ Update Category.........................
                
@admin_required
@login_required(login_url="/Admin_app/")
@never_cache                
def Update_category(request,id):
    
    try:
        if request.method == 'POST':
            name=request.POST.get("category_name")
            
            if Category.objects.filter(name=name).exists():
                
                messages.error(request, "This Category Alredy Exist")
                return redirect("category_list")
            
            Category.objects.filter(id=id).update(name=name)
        
        return redirect("category_list")
    
    except TypeError:
        return render(request,'Admin/admin_404.html')
    
                
                # ................End  Update Category.................
                
                # ................Add Category.........................
 
@admin_required
@login_required(login_url="/Admin_app/")
@never_cache                
def Add_category(request):
    try:
        
    
        if request.method == 'POST':
            name=request.POST.get("category_name")
            
            if  Category.objects.filter(name=name).exists():
                
                messages.error(request, "This Category Alredy Exist")
                return redirect("category_list")
                
            
            Category.objects.create(name=name)
            
            return redirect("category_list")
        
    except TypeError:
        return render(request,'Admin/admin_404.html')
    
                # ................End  Add Category.........................
                
                 # ................Sub Category.........................
                 
@admin_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/Admin_app/")
@never_cache    
def Sub_category(request):
    try:
        sub=Sub_Category.objects.all()
        main = Category.objects.all()       
        today = datetime.today().date()
  
        off=Offer.objects.filter(end_date__gte=today,is_delete=True)
         

        context={
            'sub':sub,
            'main':main,
             'off' : off,
            
        }

        return render(request,"admin/sub_category.html",context)
    except TypeError:
        return render(request,'Admin/admin_404.html')
                 
                  # ................End sub Category.........................
                  
                  # ................Sub Category Status Change.........................

@admin_required
@login_required(login_url="/Admin_app/")
@never_cache                  
def Status_Change(request,id):
    
    try:
        status=Sub_Category.objects.get(id=id)
        
        if not status.is_deleted:
            
            status.is_deleted=True
            status.save()
        else:
            
            status.is_deleted = False
            status.save()
            
        return redirect("sub_category") 
    except TypeError:
        return render(request,'Admin/admin_404.html')
    
    
                  # ................Sub Category Status Change.........................
                  
                   # ................Sub Update Category .........................

@admin_required
@login_required(login_url="/Admin_app/")
@never_cache                   
def Update_Sub_Category(request,id):
    
    try:
        
        if request.method == 'POST':
            
            name=request.POST.get("category_name")
            
            if  Sub_Category.objects.filter(name=name).exists():
                
                messages.error(request, " Sub Category Alredy Exist")
                return redirect("sub_category")
            
            Sub_Category.objects.filter(id=id).update(name=name)
            
            return redirect("sub_category") 
    except TypeError:
        return render(request,'Admin/admin_404.html')
    
                   
                    # ................End Update Sub Category .........................
                    
                    # ................Delete Sub Category .........................
@admin_required
@login_required(login_url="/Admin_app/")
@never_cache                    
def Delete_Sub_Category(request,id):
    
    try:
        
        sub=Sub_Category.objects.get(id=id)
        sub.delete()
        
        return redirect("sub_category")
    except TypeError:
        return render(request,'Admin/admin_404.html')
    
    
                    
                    # ................Delete Sub Category .........................
                    
                    # ................Add Sub Category .........................


@admin_required
@login_required(login_url="/Admin_app/")
@never_cache 
def Add_Sub_Category(request):
    try:
    
        if request.method == 'POST' :
            sub=request.POST.get("category_name")
            cate=request.POST.get("category_type")
        
        if  Sub_Category.objects.filter(name=sub).exists():
            
            messages.error(request, " Sub Category Alredy Exist")
            return redirect("sub_category")
        
        id=Category.objects.get(id=cate)
        Sub_Category.objects.create(name=sub,category=id)
        
        return redirect("sub_category") 
    except TypeError:
        return render(request,'Admin/admin_404.html')                        
        
                    
                    # ................End Add Sub Category .........................
                    
                    # ................Product .........................
@admin_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/Admin_app/")
@never_cache    
def Product_list(request):
    try:
        pro=Product.objects.all()
        sub=Sub_Category.objects.all()
        img=Product_image.objects.all().prefetch_related("product_set")
        
        
        context={
            'pro' : pro,
            'sub' : sub,
            'img': img
        }
        
        return render(request,"admin/Product.html",context)
    
    except TypeError:
        return render(request,'Admin/admin_404.html')
                    
                    
                    # ................End Product .........................
                    
                    # ................ Product Status.........................

@admin_required
@login_required(login_url="/Admin_app/")
@never_cache                     
def Product_Status(request,id):
   
    try:
        status=Product.objects.get(id=id)
        value=Product_size.objects.all()
        
        for i in value:
            print(i.product)
            if status == i.product:
            
                    if not status.is_deleted:
                        
                        status.is_deleted = True
                        status.save()
                        return redirect("product_list")
                    else:
                        
                        status.is_deleted = False
                        status.save()
                        return redirect("product_list")
        else:
            messages.error(request, "Please add any size")
            return redirect("product_list")
    except TypeError:
        return render(request,'Admin/admin_404.html')
                    
                    # ................End Product Status.........................
                    
                    # ................Add Product .........................
                    
# from django.core.files.base import ContentFile 

@admin_required
@login_required(login_url="/Admin_app/")
@never_cache                    
def Add_Product(request):
    
    try:
        
        if request.method == "POST" :
            
            name=request.POST.get("product_name")
            price=int(request.POST.get("price"))
            discount=int(request.POST.get("discount"))
            sub_category=request.POST.get("category_type")
            description=request.POST.get("description")
            m_image=request.FILES.get("m_image")
            r_images=request.FILES.getlist("r_images")
    
            offer=0
            if int(price) < 1:
                
                messages.error(request, "Invalid Price . Price Should Be Above Zero ")
                return redirect("product_list")
            
            elif int(discount) < 0 :
                
                messages.error(request, "Invalid Discound . Discound Should Be Zero or  Above Zero ")
                return redirect("product_list")
            
            elif discount < 0:
                
                messages.error(request, "Invalid Discound . Discound Should Be Zero or Above Zero ")
                return redirect("product_list")
            
            elif discount>=1:
                
                dis=(price*discount)//100
                
                if dis > price//2:
                    
                    messages.error(request, "Invalid Discound . Discound Should Be less than 50% ")
                    return redirect("product_list")
                else:   
                    
                   offer=(price-dis)  
            
                
            sub=Sub_Category.objects.get(id=sub_category)
            pro_id=Product.objects.create(name=name,
                                        price=price,
                                        offer_price=offer,
                                        discount=discount,
                                        sub_category=sub,
                                        description=description,
                                        image=m_image)
    
        
            for i in range(len(r_images)):
                
                Product_image.objects.create(product=pro_id,image_url=r_images[i])
                
            return redirect("product_list") 
        
    except TypeError:
        return render(request,'Admin/admin_404.html')
                    
                    # ................End Add Product .........................
                    
                    
                    # ................Delete Product .........................

@admin_required
@login_required(login_url="/Admin_app/")
@never_cache                     
def Delete_Product(request,id):
    
    try:
        pro=Product.objects.get(id=id)
        pro.delete()
        
        return redirect("product_list")
                    
    except TypeError:
        return render(request,'Admin/admin_404.html')                
                    # ................End Delete Product .........................
                    
                    # ................Update Product .........................

@admin_required
@login_required(login_url="/Admin_app/")
@never_cache                     
def Update_Product(request,id):
    
    try:
        if request.method == "POST" :
            
            up= Product.objects.get(id=id)
            
            name=request.POST.get("product_name")
            price=int(request.POST.get("price"))
            discount=int(request.POST.get("discount"))
            sub_category=request.POST.get("category_type")
            description=request.POST.get("description")
            image=request.FILES.get("image")
            r_image=request.FILES.getlist("related_images")
            delete=request.POST.getlist("selected_images")
              
           
            offer=0
            if int(price) < 1:
                
                messages.error(request, "Invalid Price . Price Should Be Above Zero ")
                return redirect("product_list")
            
            elif discount < 0:
                
                messages.error(request, "Invalid Discound . Discound Should Be Zero or Above Zero ")
                return redirect("product_list")
            
            elif discount>=1:
                
                dis=(price*discount)//100
                
                if dis > price//2:
                    
                    messages.error(request, "Invalid Discound . Discound Should Be less than 50% ")
                    return redirect("product_list")
                else:   
                    
                   offer=(price-dis)  
            
            
            sub=Sub_Category.objects.get(id=sub_category)
      
            
            up.name=name
            up.price=price
            up.offer_price=offer
            up.discount=discount
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
    except TypeError:
        return render(request,'Admin/admin_404.html')
                    
                    # ................End Update Product .........................
                    
                    # ................ADD SIZE .........................


@admin_required
@login_required(login_url="/Admin_app/")
@never_cache             
def Add_Size(request,id):
    try:
    
        if request.method == "POST":
            
            size=request.POST.get("size")
            stock=request.POST.get("stock")
            
        
            if int(size) <= 0 or int(stock) <= 0 :
                    
                    messages.error(request, "Invalid Size or Stock .Size and Stock Should Be Above Zero ")
                    return redirect("product_list")
                
            else:
                value=Product.objects.get(id=id)
                if Product_size.objects.filter(size=size,product=value).exists():
                    
                    messages.error(request, "This size already listed")
                    return redirect("product_list")
                
                else:
                        value=Product.objects.get(id=id)
                        
                        Product_size.objects.create(size=size,stock=stock,product=value)
            
        return redirect("product_list")
    except TypeError:
        return render(request,'Admin/admin_404.html')

                    # ................END ADD SIZE .........................
                    
                     # ................EDIT SIZE .........................
                     
@admin_required
@login_required(login_url="/Admin_app/")
@never_cache 
def Edit_Size(request,id):
    
    try:
            
        if request.method == 'POST':
            
            for size_obj in Product_size.objects.filter(product_id=id):
                
                size = request.POST.get('size' + str(size_obj.id))
                stock = request.POST.get('stock' + str(size_obj.id))
                
                if int(size) < 0 or int(stock) < 0 :
                    
                    messages.error(request, "Invalid Size or Stock .Size and Stock Should Be Above Zero ")
                    return redirect("product_list")
                
                else:
                    size_obj.stock=stock 
                    size_obj.size=size 
                    size_obj.save()

            
        return redirect("product_list")
    except TypeError:
        return render(request,'Admin/admin_404.html')
                    
                    # ................END EDIT SIZE .........................
                    
                    
                    # ................USER ORDERS .........................

@admin_required
@login_required(login_url="/Admin_app/")
@never_cache                     
def User_Orders(request):
    
    try:
    
        order=Order.objects.all()
        
        addresses=[]
        for i in order:
            
            pairs = i.user_address.strip('{}').split(',')        
            my_dict = {}
            for pair in pairs:
                key, value = pair.split(':')
                my_dict[key.strip(" '")] = value.strip(" '")
                
                address = {'house': my_dict.get('house', ''),
                'street': my_dict.get('street', ''),
                'city': my_dict.get('city', ''),
                'country': my_dict.get('country', ''),
                'pin_code': my_dict.get('pin_code', ''),
                'location': my_dict.get('location', ''),
                'phone': my_dict.get('phone', ''),
                'name': my_dict.get('name', ''),
            }
            
            addresses.append({ 'address': address})
            value=zip(order,addresses)
        
        context={
            'value' : value,
        }
        
        return render(request,'Admin/user_orders.html',context)
    except TypeError:
        return render(request,'Admin/admin_404.html')
                    
                    # ................END USER ORDERS  .........................
                    
                    # ................ USER ORDER LIST .........................
                    
@admin_required
@login_required(login_url="/Admin_app/")
@never_cache 
def Order_List(request,id):
    try:
        order=Order.objects.get(id=id)
        item=Order_Items.objects.filter(order_id=id)
            
        context={
            'order' : order,
            'item' : item,
        }
        
        
        return render(request,'Admin/order_list.html',context)
    except TypeError:
        return render(request,'Admin/admin_404.html')
                    
                    # ................END USER ORDER LIST .........................
                    
                    # ................ORDER STATUS .........................
                    
@admin_required
@login_required(login_url="/Admin_app/")
@never_cache 
def Order_Status(request,id):
    
    try:
    
        if request.method =='POST':
            
            action=request.POST.get("action")
        
        order=Order.objects.get(id=id)
        date=timezone.now()
        if action and action != 'refunded':
            
            order.status= action
            order.status_date=date
            order.save()
            
        
        return redirect('user_orders')
    except TypeError:
        return render(request,'Admin/admin_404.html')
                    
                    # ................END ORDER STATUS .........................
                    
                    # ................SALES REPORTS .........................
                    
                    

@never_cache                   
def Sales_Report(request):
    
    try: 
        
            if request.method == "POST":
                
                    start_date=request.POST.get("startDate")
                    end_date=request.POST.get("endDate")
            
                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename="sales_Reports.pdf"'

                    buffer = BytesIO()
                    p = canvas.Canvas(buffer)

                    p.drawString(250, 650, "Sales Report")


                    # Display information above the table
                    p.drawString(100,600, f"Sale Started : {start_date}")
                    p.drawString(100,580, f"Sale ended : {end_date}")
                    
                    p.drawString(260, 560, "Transactions")
                    
                    total_sale=Order.objects.filter(status__in=['pending','processing','shipped','delivered'], created_date__range=(start_date, end_date)).aggregate(total=Sum('total_amount'))
                    all_amount=Order.objects.filter(created_date__range=(start_date, end_date)).aggregate(total=Sum("total_amount"))
                    cod_total=Order.objects.filter(payment_type="cashOnDelivery", created_date__range=(start_date, end_date),status__in=['pending','processing','shipped','delivered']).aggregate(total=Sum('total_amount'))
                    upi_total=Order.objects.filter(payment_type="paid by Razorpay",created_date__range=(start_date, end_date),status__in=['pending','processing','shipped','delivered']).aggregate(total=Sum('total_amount'))
                    # Create a table and set its style
                    data = [['Cash on Delivery', 'Online payment','Total','total revenue']]
                    data.append([cod_total['total'],upi_total['total'],total_sale['total'],all_amount['total']])

                    table = Table(data, colWidths=[100, 80, 80, 80])
                    style = TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ])
                    table.setStyle(style)

                    # Draw the table on the PDF
                    table.wrapOn(p, 0, 0)
                    table.drawOn(p, 150, 500)  
                    
                    p.drawString(250, 460, "Orders")
                    
                    pending=Order.objects.filter(status='pending',created_date__range=(start_date, end_date)).aggregate(total=Count("status"))
                    processing=Order.objects.filter(status='processing',created_date__range=(start_date, end_date)).aggregate(total=Count("status"))
                    shipped=Order.objects.filter(status='shipped',created_date__range=(start_date, end_date)).aggregate(total=Count("status"))
                    delivered=Order.objects.filter(status='delivered',created_date__range=(start_date, end_date)).aggregate(total=Count("status"))
                    cancelled=Order.objects.filter(status='cancelled',created_date__range=(start_date, end_date)).aggregate(total=Count("status"))
                    refund=Order.objects.filter(status='refunded',created_date__range=(start_date, end_date)).aggregate(total=Count("status"))
                    
                    all=Order.objects.filter(created_date__range=(start_date, end_date)).aggregate(total=Count('id'))

                    
                    data = [['Pending','Processing','Shipped','Delivered','Cancelled','Refunded','Total Orders']]
                    data.append([pending['total'],processing['total'],shipped['total'],delivered['total'],cancelled['total'],refund['total'],all['total'],])

                    table = Table(data, colWidths=[80, 80, 80, 80, 80, 80, 80])
                    style = TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ])
                    table.setStyle(style)

                    # Draw the table on the PDF
                    table.wrapOn(p, 0, 0)
                    table.drawOn(p, 25, 400) 
                    
                    p.drawString(250, 360, "Sub Catogery Orders")
                    
                    adidas = Order_Items.objects.filter(order__created_date__range=(start_date,end_date),Sub_Category="2").aggregate(total=Coalesce(Sum('qty'), Value(0)))            
                    puma= Order_Items.objects.filter(order__created_date__range=(start_date,end_date),Sub_Category="1").aggregate(total=Coalesce(Sum('qty'), Value(0)))
                    nike= Order_Items.objects.filter(order__created_date__range=(start_date,end_date),Sub_Category="3").aggregate(total=Coalesce(Sum('qty'), Value(0)))
                    
                
                    total=adidas['total']+puma['total']+nike['total']
                
                        
                        
                    
                    data = [['Adidas','Puma','Nike','Total']]
                    data.append([adidas['total'],puma['total'],nike['total'],total])

                    table = Table(data, colWidths=[80, 80, 80, 80])
                    style = TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ])
                    table.setStyle(style)

                    # Draw the table on the PDF
                    table.wrapOn(p, 0, 0)
                    table.drawOn(p, 150, 300) 
                    
                    p.drawString(250, 250,"Product summary")
                        
                    data = [['Product','Quantity','Price',]]
                    pro=Product.objects.all()
                    for i in pro:
                        product=Order_Items.objects.filter(order__created_date__range=(start_date,end_date),product=i.id).aggregate(total=Sum('qty'))
                        
                        data.append([i.name,product['total'],i.price])

                        table = Table(data, colWidths=[80, 80, 80])
                        style = TableStyle([
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ])
                        table.setStyle(style)

                        # Draw the table on the PDF
                    table.wrapOn(p, 0, 0)
                    table.drawOn(p, 150, 100) 
                        
                    # Close the PDF object cleanly.
                    p.showPage()
                    p.save()

                    # Get the value of the BytesIO buffer and write it to the response.
                    pdf = buffer.getvalue()
                    buffer.close()
                    response.write(pdf)
                    return response
        
            return redirect('admin_dashbord')
    except:
        return render(request,'Admin/admin_404.html')
                    
                    # ................END SALES REPORTS.........................
                    
                     # ................OFFERS PAGE.........................

@admin_required
@login_required(login_url="/Admin_app/")
@never_cache                      
def Offers(request):
    
    
    off=Offer.objects.all()
    context={
        'offer' : off
    }
    
    return render(request,'Admin/offers.html',context)

                     
                      # ................END OFFERS PAGE.........................
                      
                      
                      # ................CREATE OFFERS PAGE.........................
@admin_required
@login_required(login_url="/Admin_app/")
@never_cache                      
def Creat_Offer(request):
    
        if request.method == 'POST':
            name=request.POST.get("category_name")
            disc=request.POST.get("discount")
            s_date=request.POST.get("start_date")
            e_date=request.POST.get("end_date")
            
            pattern = r'^[a-zA-Z0-9].*'
            
            s_date=datetime.strptime(s_date, '%Y-%m-%d').date()
            e_date=datetime.strptime(e_date, '%Y-%m-%d').date()
            today = datetime.today().date()
            print(today)
            
            if not re.match(pattern,name or disc ):
            
                messages.error(request,"Please Enter Valid inputs")
                return redirect('offers')
            
            elif int(disc) < 0 or int(disc) > 80:
                
                messages.error(request,"Invalid Discound . Discound Should Be Zero and Less Than 80%")
                return redirect('offers')
            
            elif s_date < today or e_date < today :
                
                messages.error(request," Invalid Date.Start Date and End Date Should Be Today or  Above Today")
                return redirect('offers')
            
            elif s_date > e_date:
                
                messages.error(request," Invalid Date. End Date Should Be Start Date or  Above Start Date")
                return redirect('offers')
            
            elif Offer.objects.filter(name=name).exists():
                
                messages.error(request," Invalid Offer. Offer Name already added")
                return redirect('offers')
            else:
                
                Offer.objects.create(name=name,
                            discount=disc,
                            start_date=s_date,
                            end_date=e_date)
                
                return redirect('offers')
                
        return redirect('offers')
    
    # ................ END CREATE OFFERS PAGE.........................
    
    
     # ................DELETE OFFERS .........................

@admin_required
@login_required(login_url="/Admin_app/")
@never_cache 
def Delete_Offer(request,id):
    
    Offer.objects.get(id=id).delete()
    return redirect('offers')
    
 # ................END DELETE OFFERS .........................
 
 
 # ................OFFERS STATUS CHANGING   .........................
 
@admin_required
@login_required(login_url="/Admin_app/")
@never_cache 
def Offer_Status(request,id):
    
    off=Offer.objects.get(id=id)
    
    if off.is_delete:
        
        off.is_delete=False
        off.save()
        
    else:
        
        off.is_delete=True
        off.save()
    
    return redirect('offers')

 # ................END OFFERS STATUS CHANGING.........................
 
 
 # ................UPDATE OFFERS.........................
 
@admin_required
@login_required(login_url="/Admin_app/")
@never_cache 
def Update_Offer(request):
    
    if request.method == "POST":
            
            id=request.POST.get("id")
            name=request.POST.get("name")
            off=request.POST.get("off")
            s_date=request.POST.get("s_date")
            e_date=request.POST.get("e_date")
        
        
            pattern = r'^[a-zA-Z0-9].*'
            
            s_date=datetime.strptime(s_date, '%Y-%m-%d').date()
            e_date=datetime.strptime(e_date, '%Y-%m-%d').date()
            today = datetime.today().date()
            
            if not re.match(pattern,name or off ):
            
                messages.error(request,"Please Enter Valid inputs")
                return redirect('offers')
            
            elif int(off) < 0 or int(off) > 80:
                
                messages.error(request,"Invalid Discound . Discound Should Be Zero and Less Than 80%")
                return redirect('offers')
            
            elif s_date < today or e_date < today:
                
                messages.error(request," Invalid Date. Date Should Be Today or  Above Today")
                return redirect('offers')
            
            elif s_date > e_date:
                
                messages.error(request," Invalid Date. End Date Should Be Start Date or  Above Start Date")
                return redirect('offers')
            
            value=Offer.objects.exclude(id=id)
            if value.filter(name=name):
                
                messages.error(request," Invalid Offer. Offer Name already added")
                return redirect('offers')
            
            elif Offer.objects.get(id=id) :
                 
                Offer.objects.filter(id=id).update(name=name,
                                                discount=off,
                                                start_date=s_date,
                                                end_date=e_date)
                
                return redirect('offers')
       
    return redirect('offers')
 
 # ................UPDATE OFFERS.........................
 
 # ................ ADD OFFERS IN SUB CATEGORY.........................
 
def Add_Offer(request):
    
    if request.method == "POST":
        
        id=request.POST.get("id")
        offer=request.POST.get("offer_id")
      
        if offer and offer != '0':
            
            Sub_Category.objects.filter(id=id).update(offer=offer)
            
       
    return redirect("sub_category") 
 
 # ................ END ADD OFFERS IN SUB CATEGORY.........................
 
def Offer_Remove(request,id):
    
    sub=Sub_Category.objects.get(id=id)
    if sub.offer:
        sub.offer=None
        sub.save()
    
    return redirect("sub_category")