from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.cache import  never_cache,cache_control
from django.contrib.auth.decorators import login_required
from Admin_app.models import *
from user_app.models import *
from . models import *
from django.shortcuts import get_object_or_404
from django.contrib import messages
import re 
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import *
import uuid
import razorpay
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors     


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

@login_required(login_url='/user_app/Login/')
@never_cache
def User_Profile(request,id):
    
    if request.user.is_authenticated:
        
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
                     
@login_required(login_url='/user_app/Login/')
@never_cache                
def Addresses(request):    
    
    if request.user.is_authenticated:
        
        user=CustomUser.objects.get(email=request.user)
        value=User_Address.objects.filter(customuser=user.id)
        
        context={
            
            'value' : value
        }
    
    
        return render(request,'dashbord/address.html',context)
    return redirect('user_profile')


         # .................END ADDRESS AND ADD ADDRESS......................
         
          # ................. ADD ADDRESS......................
          
def Add_Address(request):
    
    
    if request.user.is_authenticated:
    
        user=CustomUser.objects.get(email=request.user)
        
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
                
                
                pattern = r'^[a-zA-Z0-9].*'
                pattern_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                pattern_Phone= r'^\d{3}-?\d{3}-?\d{4}$'
                    
                if not (name or email or phone or house or street or city or country or pin_code or location):
                        messages.error(request, "please Fill Required Field")
                        return redirect("addresses")
                    
                if not all(re.match(pattern, value) and value.strip() for value in [name, email, phone, house, street, city,country, state, pin_code, location,]):
                        messages.error(request, "Please Enter Valid values")
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
    return redirect('login')
    
           # .................END ADD ADDRESS......................
         
         # .................DELETE ADDRESS......................
         
def Delete_Address(request,id):
    
        if id:
           
           User_Address.objects.filter(id=id).delete()
           
           
           return redirect("addresses")
        
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
            
            pattern = r'^[a-zA-Z0-9].*'
            pattern_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            pattern_Phone= r'^\d{3}-?\d{3}-?\d{4}$'
                
            if not (E_name or E_email or E_phone or E_house or E_street or E_city or E_country or E_pin_code or E_location):
                    messages.error(request, "please Fill Required Field")
                    return redirect("addresses")
                
            if not all(re.match(pattern, value) and value.strip() for value in [E_name, E_house, E_street, E_city, E_country, E_pin_code, E_location]):
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
         
         # .................ADD TO CART......................

@login_required(login_url='/user_app/Login/')
@never_cache   
def Add_to_Cart(request):
    
    if request.method == "POST":
        if request.user.is_authenticated:
            pro_id=request.POST.get('product_id')
            pro_size=request.POST.get('product_size')
            product = Product.objects.get(id=pro_id)
            
            product_check = Product.objects.get(id=pro_id)
            if (pro_size):
                    if(product_check):
                        
                        if (Cart.objects.filter(customuser=request.user,product=pro_id,size=pro_size)):
                            
                            return JsonResponse({'status' :"Product already in  Cart"})
                        else:
                            
                            pro_qty=request.POST.get('product_qty')
                            
                            total= int(product_check.price) * int(pro_qty)
                            
                            Cart.objects.create(customuser=request.user,
                                                product=product,
                                                size=pro_size,
                                                qty=pro_qty,
                                                price=int(product_check.price),
                                                total_price=total)
                            
                            return JsonResponse({'status' :"Product added successfully"})

                        
                    else:
                        return JsonResponse({'status' :"No such product found"})
            else:
                
                return JsonResponse({'status' :"Please select Your Size"})
                
                        
        else:
                    
            messages.error(request,"Login to Continue")
            return redirect("login")
            
        
    
    return redirect("view_product") 

         # .................END ADD TO CART......................
         
         
          # .................User CART......................
          
@login_required(login_url='/user_app/Login/')
@never_cache          
def User_Cart(request):
    
    if request.user.is_authenticated:
    
            cart=Cart.objects.filter(customuser=request.user)
            
            sub=request.session.get("sub_total")
            
            if not sub :
                sub_total=0
                for i in cart:
                
                    sub_total += int(i.total_price)
                request.session["sub_total"]=sub_total
                sub=request.session.get("sub_total")
            else:
                sub_total=0
                for i in cart:
                
                    sub_total += int(i.total_price)
                request.session["sub_total"]=sub_total
                sub=request.session.get("sub_total")
                
                
            
            context={
                
                'cart':cart,
                'sub_totel' : sub,
            }
            
            
            
            return render(request,'dashbord/cart.html',context)
    return redirect('login')
                
           # .................END USER CART......................
           
           # .................UPDATE AND STOCK MANAGE, TOTAL PRICE, SUB_TOTAL  CART......................
           
@never_cache
@require_POST
def update_quantity_view(request):
    
        cart_item_id = request.POST.get('cartItemId')
        new_quantity = int(request.POST.get('newQuantity'))
        
        if "sub_total" in request.session:
            
            del request.session["sub_total"]
        
        cart_item = get_object_or_404(Cart, id=cart_item_id)
        
        stock=Product_size.objects.get(size=cart_item.size,product=cart_item.product)
        
        if stock is not None and new_quantity > stock.stock :
            
            return JsonResponse({'error': f'Not enough stock available. Current stock: {stock.stock}'}, status=400)
    
    
        total=int(cart_item.price) * int(new_quantity)
        
        if stock.stock >= new_quantity:
        
                cart_item.qty = new_quantity
                cart_item.total_price = total
                cart_item.save()
                
                total_item=Cart.objects.filter(customuser=request.user)
                sub_total = 0
                
                for i in total_item:
                    
                    sub_total += int(i.total_price)
                
                
                cart_subtotal=request.session["sub_total"]=sub_total
                
                current_stock=stock.stock
                
                return JsonResponse({'success': True,'total_price': total,'cart_subtotal2w': cart_subtotal,'current_stock': current_stock})
            
        else:
            
            total_item=Cart.objects.filter(customuser=request.user)
            sub_total = 0
                
            for i in total_item:
                    
                sub_total += int(i.total_price)
                
                
            cart_subtotal=request.session["sub_total"]=sub_total
            return JsonResponse({'error': f'Not enough stock available. Current stock: {stock.stock}'}, status=400)
        
        
         # ................. END UPDATE AND STOCK MANAGE, TOTAL PRICE, SUB_TOTAL  CART......................
         
          # .................DELETE PRODUCT FROM CART......................
        
        
@never_cache
def Delete_Cart(request,product_id):
    
        value=Cart.objects.get(id=product_id)
        
        if "sub_total" in request.session:
        
            sub=request.session.get("sub_total")
            print(value.total_price)
            print(sub)
            
            sub_total=  int(sub) - int(value.total_price)

            print(sub_total)
            
            if "sub_total" in request.session:
                del request.session["sub_total"]
                

            request.session["sub_total"]=sub_total
            value.delete()
        
        return redirect('user_cart')
   
       # .................END DELETE PRODUCT FROM CART......................
       
        # .................CHECKOUT......................
        
@login_required(login_url='/user_app/Login/')
@never_cache       
def Checkout(request):
    
        if  request.user.is_authenticated:       
              
                value=Cart.objects.filter(customuser=request.user)
                for i in value:
                    
                    pro=Product_size.objects.filter(product=i.product,size=i.size)
                    
                    for j in pro:
                        
                        if j.stock < i.qty:
                            
                            messages.error(request,f"{i.product.name} out stock please choose any another product")
                            return redirect("user_cart")
                        
                    
                user=request.user
                value=Cart.objects.filter(customuser=user)
                sub_total=request.session.get("sub_total")
                address=User_Address.objects.filter( customuser=user)
                context={
                    
                    'value' :value,
                    'sub_total':sub_total,
                    'address' : address,
                }
                
                
                return render(request,'dashbord/checkout.html',context)
        return redirect('login')
        
        # .................END CHECKOUT......................
        
        
        # ................. EDIT CHECKOUT ADDRESS......................
@never_cache
def Checkout_Edit_Address(request):
    
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
            
 
            pattern = r'^[a-zA-Z0-9].*'
            pattern_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            pattern_Phone= r'^\d{3}-?\d{3}-?\d{4}$'
                
            if not (E_name or E_email or E_phone or E_house or E_street or E_city or E_country or E_pin_code or E_location):
                    messages.error(request, "please Fill Required Field")
                    return redirect("checkout")
                
            if not all(re.match(pattern, value) and value.strip() for value in [E_name, E_house, E_street, E_city, E_country, E_pin_code, E_location]):
                    messages.error(request,"Please Enter Valid values")
                    return redirect("checkout") 
                
            elif not re.match(pattern_email,E_email):
                    messages.error(request,"Please enter valid email address")
                    return redirect("checkout")
                
                # elif CustomUser.objects.filter(email=email).exists():
                #     messages.error(request,"Email already exists")
                #     return render(request,'dashbord/profile.html')
                
            elif not re.match(pattern_Phone,E_phone):
                    messages.error(request,"Please enter valid Phone number")
                    return redirect("checkout")
                
            
        
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
        

            return redirect("checkout")
        
        # .................END EDIT CHECKOUT ADDRESS......................
        
        
        # .................ADD CHECKOUT ADDRESS......................
@never_cache       
def Checkout_Add_Address(request):
    
    
    if request.user.is_authenticated:
    
    
        user=CustomUser.objects.get(email=request.user)
        
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
                
                pattern = r'^[a-zA-Z0-9].*'
                pattern_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                pattern_Phone= r'^\d{3}-?\d{3}-?\d{4}$'
                    
                if not (name or email or phone or house or street or city or country or pin_code or location):
                        messages.error(request, "please Fill Required Field")
                        return redirect("checkout")
                    
                if not all(re.match(pattern, value) and value.strip() for value in [name, email, phone, house, country, state, street , city, pin_code, location]):
                        messages.error(request,"Please Enter Valid values")
                        return redirect("checkout") 
                    
                elif not re.match(pattern_email,email):
                        messages.error(request,"Please enter valid email address")
                        return redirect("checkout")
                    
                    # elif CustomUser.objects.filter(email=email).exists():
                    #     messages.error(request,"Email already exists")
                    #     return render(request,'dashbord/profile.html')
                    
                elif not re.match(pattern_Phone,phone):
                        messages.error(request,"Please enter valid Phone number")
                        return redirect("checkout")
                    
                
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
        
        
                return redirect("checkout")
        
        
        return redirect("checkout")
    return redirect("login")
        
        
        # .................END ADD CHECKOUT ADDRESS......................
        
        
        # .................USER ORDER......................
        
@never_cache        
def User_Order(request):
    
    
    if  request.user.is_authenticated:
        
        if request.method == 'POST':
            
            user=int(CustomUser.objects.get(email=request.user))
            user_id=CustomUser.objects.get(id=user)
          
            print(user_id.id)
            address=request.POST.get('address')
            payment_method=request.POST.get('paymentMethod')
            
            total=Cart.objects.filter(customuser=user_id).aggregate(total=Sum('total_price'))
            

            address=User_Address.objects.filter(id=address)
            for j in address:
               user_add={'name' :j.name , 'email' : j.email, 'phone' : j.phone, 
                     'house' :j.house, 'street': j.street, 'city': j.city, 
                     'state':j.state, 'country':j.country, 'pin_code':j.pin_code,
                     'location': j.location} 
               
               
            # ..................stock rechecking.................
            
             
           
            value=Cart.objects.filter(customuser=request.user)
            for i in value:
                    
                    pro=Product_size.objects.filter(product=i.product,size=i.size)
                    
                    for j in pro:
                        if j.stock < i.qty:
                            
                            messages.error(request,f"{i.product.name} out stock please choose any another product")
                            return redirect("user_cart")
                        
                        # ........... CASH ON DELIVERY ............
                        
          
            
            if  payment_method == 'cashOnDelivery':    
                
               
                for i in value:
                                                    
                        for j in pro:
                                                
                           if j.stock >= i.qty:
                                                        
                                new_stock=j.stock-i.qty
                                Product_size.objects.filter(product=i.product,size=i.size).update(stock=new_stock)
                                                        
                                    
                                
                                    #    ...............order_id genarating.............
                                    
                                    
                                unique_id = uuid.uuid4()
                                order_id = str(unique_id)[:8]
                            
                                    
                                    # ..................order creating.................
                                    
                                print(user_id) 
                                Order.objects.create(user = user_id,
                                                    user_address =user_add,
                                                    total_amount = total['total'],
                                                    payment_type = payment_method,
                                                    order_id = order_id 
                                                        )
                                
                                id=Order.objects.get(order_id=order_id)
                                value=Cart.objects.filter(customuser=user_id)
                                request.session['order_id']=id.id
                                    
                                    
                                for i in value:
                                    
                                    Order_Items.objects.create(order=id,
                                                            product=i.product,
                                                            Sub_Category=i.product.sub_category,
                                                            qty=i.qty,
                                                            size=i.size,
                                                            price=i.price,
                                                            total_price=i.total_price)
                                        
                                    
                                
                                Cart.objects.filter(customuser=user_id).delete()
        
                                return redirect('confirmation')
                            
            if request.method == "POST":    
                          
                    payment_method=request.POST.get("payment_mode")
                    address_id=request.POST.get("address_id")
                    
                    if payment_method == "paid by Razorpay":
                        
                        address=User_Address.objects.filter(id=address_id)
                        for j in address:
                            user_add={'name' :j.name , 'email' : j.email, 'phone' : j.phone, 
                                    'house' :j.house, 'street': j.street, 'city': j.city, 
                                    'state':j.state, 'country':j.country, 'pin_code':j.pin_code,
                                    'location': j.location} 
                            
                            # .................stock checking ............
                        value=Cart.objects.filter(customuser=request.user)
                        for i in value:
                                
                                pro=Product_size.objects.filter(product=i.product,size=i.size)
                                
                                for j in pro:
                                    
                                    if j.stock < i.qty:
                                        
                                        messages.error(request,f"{i.product.name} out stock please choose any another product")
                                        return redirect("user_cart")
                                    
                                    # .................stock rechecking ............
                                    
                        value=Cart.objects.filter(customuser=request.user)
                        for i in value:
                            
                            pro=Product_size.objects.filter(product=i.product,size=i.size)
                                                    
                            for j in pro:
                                                        
                                if j.stock >= i.qty:
                                                                
                                        new_stock=j.stock-i.qty
                                        Product_size.objects.filter(product=i.product,size=i.size).update(stock=new_stock)
                                                                
                                            
                                        
                                            #    ...............order_id genarating.............
                                            
                                            
                                        unique_id = uuid.uuid4()
                                        order_id = str(unique_id)[:8]
                                    
                                            
                                            # ..................order creating.................
                                            
                                            
                                        Order.objects.create(user = user_id,
                                                            user_address =user_add,
                                                            total_amount = total['total'],
                                                            payment_type = payment_method,
                                                            order_id = order_id 
                                                                )
                                        
                                        id=Order.objects.get(order_id=order_id)
                                        value=Cart.objects.filter(customuser=user_id)
                                        
                                        request.session['order_id']=id.id
                                            
                                            
                                        for i in value:
                                            
                                            Order_Items.objects.create(order=id,
                                                                    product=i.product,
                                                                    Sub_Category=i.product.sub_category,
                                                                    qty=i.qty,
                                                                    size=i.size,
                                                                    price=i.price,
                                                                    total_price=i.total_price)
                                                
                                            
                                        
                                        Cart.objects.filter(customuser=user_id).delete()
                                      
                
                                        return redirect('confirmation')
                                else:
                                    
                                    messages.error(request,f"{i.product.name} out stock please choose any another product")
                                    return redirect("user_cart")
                                
        
        # ................. END USER ORDER ......................
        
        
        # ................. ORDER CONFIRMATION ..................
@never_cache       
def Confirmation(request):
    
    id=str(request.session.get('order_id'))
    
    order=Order.objects.get(id=id)
    item=Order_Items.objects.filter(order=id)
    
    print(type(order.user_address))
    pairs = order.user_address.strip('{}').split(',')

    # Create a dictionary from the key-value pairs
    my_dict = {}
    for pair in pairs:
        key, value = pair.split(':')
        my_dict[key.strip(" '")] = value.strip(" '")
    
    context={
        'order' : order,
        'item' : item,
        'house' : my_dict['house'],
        'street' : my_dict['street'],
        'city' : my_dict['city'] ,
        'country' : my_dict['country'] 
    }
    
    
    return render(request,'dashbord/confirmation.html',context)



       # .................END ORDER CONFIRMATION ......................
       
       
       # .................MY ORDER ......................
@never_cache      
def My_Order(request):
    
    user=CustomUser.objects.get(email=request.user)
    order=Order.objects.filter(user_id=user.id)
    
    
    if order:
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
                    
                'value':value
                
                }
        
        return render(request,'dashbord/my_order.html',context)
    
    return render(request,'dashbord/my_order.html')

       
       # .................END MY ORDER ......................
       
       # ................. ORDER DETAILS......................
@never_cache      
def Order_Details(request,id):
    
    order=Order.objects.get(id=id)
    item=Order_Items.objects.filter(order_id=id)
        
    context={
        'order' : order,
        'item' : item,
    }
    
    return render(request,'dashbord/order_details.html',context)
       
       # .................END ORDER DETAILS......................
       
       # .................ORDER CANCELLATION......................
@never_cache  
def Cancellation(request,id):
    
    order=Order.objects.get(id=id)
    date=timezone.now()
    if order:
       
        if order.payment_type == 'cashOnDelivery' :
            user_order=Order_Items.objects.filter(order_id=id)
            for i in user_order:
                
                
                stock=Product_size.objects.get(product=i.product,size=i.size)
                
                stock.stock += i.qty
                stock.save()
    
            order.status= 'cancelled'
            order.status_date=date
            order.save()
            
        elif order.payment_type == 'paid by Razorpay' :
            user_order=Order_Items.objects.filter(order_id=id)
            for i in user_order:
                
                
                stock=Product_size.objects.get(product=i.product,size=i.size)
                
                stock.stock += i.qty
                stock.save()
    
            order.status= 'cancelled'
            order.status_date=date
            order.save()
    
    return redirect('my_order')
         
       
       # .................END ORDER CANCELLATION......................
       
       
       # .................RAZORPAY......................
       
@never_cache
def Pay_With_Upi(request):
       
            user=int(CustomUser.objects.get(email=request.user))
            user_id=CustomUser.objects.get(id=user)
          
          
            total=Cart.objects.filter(customuser=user_id).aggregate(total=Sum('total_price'))
            
            # .........stock cheking ...........
            
            value=Cart.objects.filter(customuser=request.user)
            for i in value:
                    
                    pro=Product_size.objects.filter(product=i.product,size=i.size)
                    
                    for j in pro:
                        
                        if j.stock < i.qty:
                            
                            messages.error(request,f"{i.product.name} out stock please choose any another product")
                            return redirect("user_cart")
            total=total['total']
            client = razorpay.Client(auth=("Rrzp_test_NqH0AQ919F3Q3B", "90Ku7HA85h4ej9uv0AptcwpK"))
           
          
                
            return JsonResponse({
                    'total_amount' : total ,'username' :user_id.username,'email' : user_id.email,'phone':user_id.ph_no,
                    })

       # .................END RAZORPAY......................
       
       # .................NEW PASSWORD......................
@login_required(login_url='/user_app/Login/')
@never_cache      
def New_Password(request):
    
        
        
    if  request.user.is_authenticated:
        
            if request.method =='POST':
                old_pass=request.POST.get("old_password")
                new_pass=request.POST.get("new_password")
                con_pass=request.POST.get("con_password")
                
                print(old_pass,new_pass,con_pass,"........234")
                
                pattern = r'^[a-zA-Z0-9].*'
                pattern_pass = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
                
                if not (old_pass and new_pass and con_pass ):
                    messages.error(request, "please Fill Required Field")
                    return render(request,"dashbord/new_password.html")
                
                elif not re.match(pattern_pass,new_pass):
                    messages.error(request,"The password is too weak")
                    return render(request,"dashbord/new_password.html")
                        
                elif new_pass != con_pass:
                    
                    messages.error(request,"New Password and confirm password doesn't match ")
                    return render(request,"dashbord/new_password.html")
                
                else:
                        try:
                            
                            
                            user= authenticate(request,email=request.user,password=old_pass)
                            
                        except Exception as e:
                            
                            messages.error(request,"Old Password doesn't match ")
                            return render(request,"dashbord/new_password.html")
                 
                        try:
                                  
                            user=CustomUser.objects.get(email=request.user)
                            hashed_password = make_password(new_pass)
                            user.password = hashed_password
                            user.save()
                                    
                            messages.success(request,"New password updated")
                            return redirect("login")
                        
                        except Exception as e:
                            return render(request,"dashbord/404.html")
                            
                            
                        
                    
    
    return render(request,"dashbord/new_password.html")

       # .................END NEW PASSWORD......................
       
       # .................USER ORDERS BILL DOWNLOADING......................
def Orders_Bill(request,id):
    
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="sales_invoice.pdf"'

        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        p.drawString(250, 650, "Sales Invoice")

        order_item = Order_Items.objects.filter(order=id)
        order = Order.objects.get(id=id)

        # Display information above the table
        p.drawString(100,605, f"Customer : {order.user.username}")
        p.drawString(100,590, f"Date : {order.created_date.strftime('%Y-%m-%d')}")
        p.drawString(100,573, f"Order id : {order.order_id}")
        

        # Create a table and set its style
        data = [['Item', 'Quantity', 'Unit Price', 'Total']]
        for item in order_item:
            data.append([item.product.name, item.qty, item.price, item.total_price])

        table = Table(data, colWidths=[150, 80, 80, 80])
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
        table.drawOn(p, 100, 500)  # Adjust the Y-coordinate as needed
        
       

        # Display "Total Amount" below the table
        # p.drawString(360,470, f"Total Amount : {order.total_amount}")

        # Close the PDF object cleanly.
        p.showPage()
        p.save()

        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

        
       
       # .................END USER ORDERS BILL DOWNLOADING......................
       
       