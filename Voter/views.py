from django.shortcuts import render,redirect
from Voter.models import VoterList,Profile,LoginKey,VoteKey,Key
from Voter.calculations import *
from Voter.otp import *
import datetime
from datetime import datetime,timedelta
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import os
from PIL import Image,UnidentifiedImageError
from io import BytesIO
from django.conf import settings
import subprocess
import cv2
import numpy as np
from django.contrib.auth.models import User
from Voter.key import *
from Voter.encrypt import *
from django.contrib.auth import authenticate,login,logout
from MAdmin.models import *
from CWAdmin.models import *
from django.contrib.auth.decorators import login_required


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
                return redirect('validate_user_otp')
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
        Key.objects.create(uid=uid,key=key)
        send_log_key(email,log_key)
        return redirect('login')
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
                login(request, user)
                if hasattr(user, 'staff_profile'):
                    if user.staff_profile.cp == 0:
                        return redirect('change_password')
                    else:
                        return redirect('cwhome')
                else:
                    messages.error(request, 'Staff profile not found.')
                    return redirect('home')  
            else:
                login(request, user)
                return redirect('home') 
        else:
            messages.error(request, 'Invalid user credentials')
    return render(request, 'login.html')

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
    request.session.pop('is_authenticated', None)
    return redirect('home')

@login_required(login_url='login')
def check_password(request):
    if request.POST:
        username=request.user.username
        password=request.POST.get('password')
        data=LoginKey.objects.get(user=username)
        data.validity=1 #used for production .remove before deployment
        data.save()
        if data.validity==1:
            salt=data.salt
            stored_password=data.key
            a=verify_key(password,salt,stored_password)
            if a:
                request.session['is_authenticated'] = True
                data.validity=0
                data.save()
                return redirect('vote')
            else:
                messages.error(request,"Incorrect Password")
        else:
            messages.error(request,"Password expired")
    return render(request,'check_password.html')

@login_required(login_url='login')
def vote(request):
    if not request.session.get('is_authenticated'):
        return redirect('check_password')
    #fetching key of user
    username=request.user.username
    name=request.user.user_profile.vid.fname
    uid=generate_log_id(username,name)
    key=Key.objects.get(uid=uid)
    vkey=VoteKey.objects.get(uid=uid)
    print((decrypt_aes(vkey.key,key.key)).decode('utf-8'))
    #completed fetching
    constituency = request.user.user_profile.vid.Constituency
    can=Candidate.objects.filter(p_constituency=constituency)
    context={'candidates':can}
    return render(request,'vote.html',context)

def help(request):
    return render(request,'help.html')

@login_required(login_url='login')
def display_candiadtes(request):
    constituency = request.user.user_profile.vid.Constituency
    can=Candidate.objects.filter(p_constituency=constituency)
    context={'candidates':can}
    return render(request,'candidates.html',context)

def decode_image(image_data):
    image_data = image_data.split(',')[1]
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return image

@login_required(login_url='login')
def candidate_details(request,pk):
    can=Candidate.objects.get(id=pk)
    context={'candidate':can}
    return render(request,'candidate_details.html',context)


def cast_vote(request, id):
    if request.method == 'POST':
        image_data = request.POST.get('image')
        if not image_data:
            messages.error(request, "No image data received")
            return redirect('vote')

        unknown_img_path = os.path.join(settings.BASE_DIR, '.tmp.jpg')

        try:
            image_data = image_data.split(',')[1]
            image = Image.open(BytesIO(base64.b64decode(image_data)))
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            cv2.imwrite(unknown_img_path, image)

            # Run face recognition
            output = subprocess.check_output(['face_recognition', db_dir, unknown_img_path])
            output = output.decode('utf-8').strip()
            name = output.split(',')[1] if ',' in output else 'unknown'
            print(name)
            
            
            if name in ['unknown_person', 'no_persons_found', 'unknown']:
                print("Authorization failed")
                messages.error(request,"Authorization failed")
            else:
                messages.success(request,"successfully authorised")
                return redirect('vote')

        except Exception as e:
            print(f"Error: {e}")
            messages.error(request,"Error occurred while recognizing the face.")

        finally:
            if os.path.exists(unknown_img_path):
                os.remove(unknown_img_path)

    return redirect('vote')