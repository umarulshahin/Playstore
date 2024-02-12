from django.db import models
from user_app.models import *
from Admin_app.models import *
# Create your models here.

class Cart(models.Model):
    
    customuser=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    qty=models.IntegerField(null=False,blank=False)
    size=models.IntegerField(null=False,blank=False)
    price=models.IntegerField(null=False,blank=False)
    total_price=models.IntegerField(null=False,blank=False)
    
class Wishlist(models.Model):
    
    customuser=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    
    