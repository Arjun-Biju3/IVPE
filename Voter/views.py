from django.shortcuts import render,redirect
from Voter.models import VoterList,Profile,LoginKey,VoteKey
from Voter.calculations import *
from Voter.otp import *
import datetime
from datetime import datetime,timedelta
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import os
from PIL import Image
from io import BytesIO
from django.conf import settings
import subprocess
import cv2
import numpy as np
from django.contrib.auth.models import User
from Voter.key import *
from Voter.encrypt import *
from django.contrib.auth import authenticate,login,logout


#folder to upload captured image
db_dir = os.path.join(settings.BASE_DIR, 'db')
if not os.path.exists(db_dir):
    os.mkdir(db_dir)

#function to render index
def home(request):
    return render(request,'index.html')

#function to display otp page
def otp_page(request):
    success_message="OTP has been send succesfully"
    messages.success(request,success_message)
    if request.POST:
        otp=request.POST.get('otp')
        res=validate_otp(request,otp)
        if res==1:
            clear_otp(request)
            adhar=request.session.get('adhar')
            return redirect('details',id=adhar)
        if res==-1:
            error_message="OTP Expired"
            messages.error(request,error_message)
        if res==0:
            error_message="Invalid OTP"
            messages.error(request,error_message)
    #resend OTP
    if request.POST and 'resend' in request.POST:
        otp=generate_otp()
        email=request.session.get('email')
        request.session['otp']=otp
        request.session['otp_expires'] = (datetime.now() + timedelta(minutes=5)).isoformat()
        send_email(email,otp)
    return render(request,'otp_page.html')

#function to render registration page
def register(request):
    if request.POST:
        adhar=request.POST.get('adhar')
        user=VoterList.objects.filter(adharNo=adhar).first()
        if user is not None:
            age=calculate_age(user.dob)
            if user.eligibility_status ==1 and user.register_status==0 and age >= 18:
                email=user.email
                #generate OTP
                otp=generate_otp()
                request.session['adhar']=adhar
                request.session['email']=email
                request.session['otp']=otp
                request.session['otp_expires'] = (datetime.now() + timedelta(minutes=5)).isoformat()
                #send mail
                send_email(email,otp)
                print(otp)
                return redirect('validate')
            else:
                error_message="You are already registered or you are not eligible"
                messages.error(request,error_message)
        else:
            error_message="Enter a valid Adhar number"
            messages.error(request,error_message)
    return render(request,'register.html')

def details(request,id):
    if request.POST:
        username=request.POST.get('username')
        password=request.POST.get('password')
        name=request.POST.get('fname')
        email=request.POST.get('email')
        #create user
        user=User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )
        person=VoterList.objects.get(adharNo=username)
        Profile.objects.create(user=user,vid=person)
        person.register_status=1
        person.save()
        #add image
        image_data = request.POST.get('image')
        image = decode_image(image_data)
        filename = os.path.join(db_dir, f'{username}.jpg')
        cv2.imwrite(filename, image)
        #generate login key and send
        log_key=generate_log_key(username,name)
        key,salt=hash_key_with_salt(log_key)
        LoginKey.objects.create(user=username,key=key,salt=salt)
        #generrate vote key and store
        uid=generate_log_id(username,name)
        Okey=generate_vote_key(username,name)
        vkey=add_string_with_random_separator(uid,Okey)
        # Generating a random key for AES-128
        key = os.urandom(16)  # Securely generated key
        Enc_key=encrypt_aes(vkey,key)
        VoteKey.objects.create(uid=uid,key=Enc_key)
        send_log_key(email,log_key)
        return redirect('home')
    user=VoterList.objects.get(adharNo=id)
    context={'user':user}
    return render(request,'details.html',context)

def user_login(request):
    if request.method == 'POST': 
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:  
            if user.is_superuser: 
                login(request, user)
                return redirect('ahome') 
            elif user.is_staff:
                login(request,user)
                if user.staff_profile.cp==0:
                    return redirect('change_password')
                else:
                    login(request,user)
                    return redirect('cwhome')
            else:
                login(request, user)
                return redirect('home') 
        else:
            messages.error(request, 'Invalid user credentials')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

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