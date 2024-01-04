from django.urls import path
from . import views

urlpatterns = [
    path('',views.Admin,name="admin_login"),
    path('admin_dashbord/',views.Admin_dashbord,name="admin_dashbord"),
    path('admin_logout/',views.Admin_logout,name="admin_logout"),
    path('user_list/',views.User_list,name="user_list"),

    

]
