from django.db import models

# Create your models here.


class Category(models.Model):
    name=models.CharField( max_length=250)
    is_deleted=models.BooleanField(default=False)
    
class Sub_Category(models.Model):
    
    name=models.CharField( max_length=250)
    category=models.ForeignKey(Category,on_delete=models.PROTECT)
    is_deleted=models.BooleanField(default=False)
    
    
