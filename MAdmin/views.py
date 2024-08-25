from django.shortcuts import render,redirect
from CWAdmin.models import *
from django.contrib.auth.models import User
from MAdmin.password import *

def admin_home(request):
    return render(request,'index2.html')

def add_cadmins(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        state = request.POST['state']
        constituency_id = request.POST['constituency']
        image = request.FILES.get('image')
        password=generate_simple_password()
    
        constituency = Constituency.objects.get(id=constituency_id)
        user = User.objects.create_user(username=email, password=password, is_staff=True)
        CWadmin.objects.create(
            fname=fname,
            lname=lname,
            email=email,
            phone=phone,
            state=state,
            user=user,
            constituency=constituency,
            image=image
        )
        send_mail(email,email,password,fname)
        return redirect('cadmins')

    constituencies = Constituency.objects.all()
    context={'constituencies':constituencies}
    
    return render(request,'add_admins.html',context)

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