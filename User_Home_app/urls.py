from django.urls import path
from . import views

urlpatterns = [
    path('',views.Dashbord,name="Dashbord"),
    
    path('all_product/',views.All_Product,name="all_product"),
    
    path('view_product/<int:id>',views.View_Product,name="view_product"),
    
    path('user_profile/<int:id>',views.User_Profile,name="user_profile"),
    
    path('edit_profile/<int:id>',views.Edit_Profile,name="edit_profile"),
    
    path('addresses/',views.Addresses,name="addresses"),
    
    path('add_address/',views.Add_Address,name="add_address"),
    
    path('delete_address/<int:id>',views.Delete_Address,name="delete_address"),
    
    path('edit_address/',views.Edit_Address,name="edit_address"),
    
    

]
