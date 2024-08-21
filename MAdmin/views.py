from django.shortcuts import render,redirect
from MAdmin.models import *

def admin_home(request):
    return render(request,'index2.html')

def add_cadmins(request):
    return render(request,'add_admins.html')

def constituency(r):
    if r.POST:
        Constituency.objects.create(
            state=r.POST.get('state'),
            name=r.POST.get('con')
            )
        return redirect('constituency')
    con=Constituency.objects.all()
    context={'con':con}
    return render(r,'constituency.html',context)

def delete_constituency(request,pk):
    data=Constituency.objects.get(pk=pk)
    data.delete()
    return redirect('constituency')