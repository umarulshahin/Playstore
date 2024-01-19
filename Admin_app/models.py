from django.db import models

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
    stock=models.IntegerField()
    sub_category=models.ForeignKey(Sub_Category,on_delete=models.CASCADE) 
    description=models.TextField()
    is_deleted = models.BooleanField(default=False)
    image =  models.ImageField(upload_to='img/product')
    
    def __bool__(self):
        return  self.is_deleted
    
    def __iter__(self):
        
        yield  self.id

    
class Product_image(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to ='img/product')
    

class Product_size(models.Model):
    size=models.CharField(max_length=50,null=True)
    stock=models.IntegerField(null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    
    
