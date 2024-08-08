from django.shortcuts import render,redirect
from Voter.models import VoterList
from Voter.calculations import *
from Voter.otp import *

api_key="427520ApBUXZ2TfOk66b4d03dP1"

def home(request):
    return render(request,'index.html')

def otp_page(request):
    if request.POST:
        pass
    return render(request,'otp_page.html')

def register(request):
    if request.POST:
        adhar=request.POST.get('adhar')
        user=VoterList.objects.get(adharNo=adhar)
        age=calculate_age(user.dob)
        if user.eligibility_status ==1 and user.register_status==0 and age >= 18:
            phone=user.phone
            otp=generate_otp()
            
      
        return redirect('validate')
    return render(request,'register.html')

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