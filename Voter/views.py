from django.shortcuts import render,redirect
from Voter.models import VoterList
from Voter.calculations import *
from Voter.otp import *
import datetime
from datetime import datetime,timedelta
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import numpy as np
import base64
import os
from PIL import Image
from io import BytesIO
from django.conf import settings
import subprocess



db_dir = os.path.join(settings.BASE_DIR, 'db')
log_path = os.path.join(settings.BASE_DIR, 'log.txt')

if not os.path.exists(db_dir):
    os.mkdir(db_dir)

def home(request):
    return render(request,'index.html')

def otp_page(request):
    success_message="OTP has been send succesfully"
    messages.success(request,success_message)
    if request.POST:
        otp=request.POST.get('otp')
        res=validate_otp(request,otp)
        if res==1:
            print("validated")
            clear_otp(request)
            adhar=request.session.get('adhar')
            return redirect('details',id=adhar)
        if res==-1:
            error_message="OTP Expired"
            messages.error(request,error_message)
        if res==0:
            error_message="Invalid OTP"
            messages.error(request,error_message)
        
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
        user=VoterList.objects.filter(adharNo=adhar).first()
        if user is not None:
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
        else:
            error_message="Enter a valid Adhar number"
            messages.error(request,error_message)
    return render(request,'register.html')

def details(request,id):
    if request.POST:
        username=request.POST.get('username')
        image_data = request.POST.get('image')
        image = decode_image(image_data)
        filename = os.path.join(db_dir, f'{username}.jpg')
        cv2.imwrite(filename, image)

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

def decode_image(image_data):
    image_data = image_data.split(',')[1]
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return image