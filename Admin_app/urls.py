from django.urls import path
from . import views

urlpatterns = [
    path('',views.Admin,name="admin_login"),
    path('admin_dashbord/',views.Admin_dashbord,name="admin_dashbord"),
    path('admin_logout/',views.Admin_logout,name="admin_logout"),
    path('user_list/',views.User_list,name="user_list"),
    path('user_block/<int:id>',views.User_block,name="user_block"),
    path('user_unblock/<int:id>',views.User_unblock,name="user_unblock"),



    

]
