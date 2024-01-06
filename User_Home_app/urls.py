from django.urls import path
from . import views

urlpatterns = [
    path('',views.Dashbord,name="Dashbord"),
    
    path('all_product/',views.All_Product,name="all_product"),
    
    path('view_product/<int:id>',views.View_Product,name="view_product")

]
