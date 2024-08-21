from django.shortcuts import render
from MAdmin.models import *

def admin_home(request):
    return render(request,'index2.html')

def add_cadmins(request):
    return render(request,'add_admins.html')

def constituency(request):
    con=Constituency.objects.all()
    context={'con':con}
    return render(request,'constituency.html',context)