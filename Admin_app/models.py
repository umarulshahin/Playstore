from django.db import models
from user_app.models import *
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    name=models.CharField( max_length=250 )
    is_deleted=models.BooleanField(default=False)
    
class Sub_Category(models.Model):
    
    name=models.CharField( max_length=250, )
    category=models.ForeignKey(Category,on_delete=models.PROTECT)
    is_deleted=models.BooleanField(default=False)
    
class Product(models.Model):
    
    name=models.CharField(max_length=250)
    price=models.BigIntegerField()
    discount=models.DecimalField( max_digits=20, decimal_places= 2,null=True)
    sub_category=models.ForeignKey(Sub_Category,on_delete=models.CASCADE) 
    description=models.TextField()
    is_deleted = models.BooleanField(default=False)
    image =  models.ImageField(upload_to='img/product')
    
    def __bool__(self):
        return  self.is_deleted
    
    def __iter__(self):
        
        return  self.id

    
class Product_image(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to ='img/product')
    

class Product_size(models.Model):
    size=models.CharField(max_length=50,null=False)
    stock=models.IntegerField(null=False)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    
    
class Order(models.Model):
    
    ORDER_STATUS = (
        
        ('pending', 'Pending'),
        ('processing','processing'),
        ('shipped','shipped'),
        ('delivered','delivered'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded','Refunded'),

    )
    
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100,null=False,unique=True)
    user_address = models.TextField(null=False)
    total_amount = models.IntegerField(null=False)
    payment_type = models.CharField(max_length=100,null=False)
    status = models.CharField(max_length=100,choices=ORDER_STATUS,default='pending')
    status_date = models.DateTimeField(default=timezone.now,null=False)
    order_id = models.CharField(max_length=100,null=False,unique=True)
    created_date =models.DateTimeField(default=timezone.now,null=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = self.id
        self.total_amount = int(self.total_amount)
    
    

class Order_Items(models.Model):
    
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    qty=models.IntegerField(null=False,blank=False)
    size=models.IntegerField(null=False,blank=False)
    price=models.IntegerField(null=False,blank=False)
    total_price=models.IntegerField(null=False,blank=False)
 
    
    
    
    
    
    
    
    
    

    
    
