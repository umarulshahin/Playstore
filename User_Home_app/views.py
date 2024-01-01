from django.shortcuts import render,HttpResponse

# Create your views here.

def Dashbord(request):
    return render(request,'dashbord/dashbord.html')
    