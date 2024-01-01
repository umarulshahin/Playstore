from django.urls import path
from . import views

urlpatterns = [
    path('Login/',views.Login,name='login'),
    path('Signup/',views.Signup,name='signup'),
    path('Signup_Otp/',views.Signup_Otp,name='signup_otp'),
    path('Forget_pass/',views.Forget_pass,name='forget_pass'),
    path('New_pass/',views.New_pass,name='new_pass'),
    path('Forget_Otp/',views.Forget_Otp,name='Forget_pass'),


]
