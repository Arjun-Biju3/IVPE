from django.shortcuts import render,redirect
from Voter.models import VoterList
from Voter.calculations import *
from Voter.otp import *
from datetime import datetime,timedelta


def home(request):
    return render(request,'index.html')

def otp_page(request):
    if request.POST:
        otp=request.POST.get('otp')
        res=validate_otp(request,otp)
        if res==1:
            print("validated")
            clear_otp(request)
            adhar=request.session.get('adhar')
            return redirect('details',id=adhar)
        if res==-1:
            print("Expired")
        if res==0:
            print("Invalid")
        
    if request.POST and 'resend' in request.POST:
        otp=generate_otp()
        email=request.session.get('email')
        request.session['otp']=otp
        request.session['otp_expires'] = (datetime.now() + timedelta(minutes=5)).isoformat()
        send_email(email,otp)
    return render(request,'otp_page.html')

def register(request):
    if request.POST:
        adhar=request.POST.get('adhar')
        user=VoterList.objects.get(adharNo=adhar)
        age=calculate_age(user.dob)
        if user.eligibility_status ==1 and user.register_status==0 and age >= 18:
            email=user.email
            otp=generate_otp()
            request.session['adhar']=adhar
            request.session['email']=email
            request.session['otp']=otp
            request.session['otp_expires'] = (datetime.now() + timedelta(minutes=5)).isoformat()
            send_email(email,otp)
            print(otp)
        return redirect('validate')
    return render(request,'register.html')

def details(request,id):
    user=VoterList.objects.get(adharNo=id)
    context={'user':user}
    return render(request,'details.html',context)

def login(request):
    return render(request,'login.html')

def logout(request):
    return render(request,'index.html')

def candidates(request):
    return render(request,'candidates.html')

def vote(request):
    return render(request,'vote.html')

def help(request):
    return render(request,'help.html')