from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    # .............. Admin.....................
    
    path('',views.Admin,name="admin_login"),
    
    path('admin_dashbord/',views.Admin_dashbord,name="admin_dashbord"),
    
    path('admin_logout/',views.Admin_logout,name="admin_logout"),
    
    # .............. End Admin.....................
    
    # .............. User List.....................
    
    path('user_list/',views.User_list,name="user_list"),
    
    path('user_block/<int:id>',views.User_block,name="user_block"),
    
    path('user_unblock/<int:id>',views.User_unblock,name="user_unblock"),
    
    # ..............End User List.....................
    
    # .............. Category.....................
    
    path('category_list/',views.Category_list,name="category_list"),
    
    path('change_status/<int:id>',views.Change_Status,name="change_status"),
    
    path('delete_category/<int:id>',views.Delete_category,name="delete_category"),
    
    path('update_category/<int:id>',views.Update_category,name="update_category"),
    
    path('add_category/',views.Add_category,name="add_category"),
    
    # ..............End Category.....................
    
    # ..............Sub Category.....................
    
    path('Sub_category/',views.Sub_category,name="sub_category"),
    
    path('status_change/<int:id>',views.Status_Change,name="status_change"),
    
    path('update_sub_category/<int:id>',views.Update_Sub_Category,name="update_sub_category"),
    
    path('delete_sub_category/<int:id>',views.Delete_Sub_Category,name="delete_sub_category"),
    
    path('add_sub_category/',views.Add_Sub_Category,name="add_sub_category"),

    
    # .............. End Sub Category.....................
    
    # .............. Product.....................
    
    path('product_list/',views.Product_list,name="product_list"),
    
    path('product_status/<int:id>',views.Product_Status,name="product_status"),
    
    path('add_product/',views.Add_Product,name="add_Product"),
    
    path('delete_product/<int:id>',views.Delete_Product,name="delete_product"),
    
    path('update_product/<int:id>',views.Update_Product,name="update_product"),

    
    # ..............End Product.....................
    
    

]

