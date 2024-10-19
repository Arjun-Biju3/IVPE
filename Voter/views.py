from django.shortcuts import render,redirect
from Voter.models import VoterList,Profile,LoginKey,VoteKey,Key,Votes
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
from django.utils import timezone
import pytz


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
        request.session['c']=0
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
                    request.session['c']=1
                    messages.error(request, 'Staff profile not found.')
                    return redirect('home')  
            else:
                login(request, user)
                return redirect('home') 
        else:
            request.session['c']=1
            messages.error(request, 'Invalid user credentials')
    c=request.session.get('c')
    return render(request, 'login.html',{'c':c})

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
    try:
        time_instance = Time.objects.get(key="start_vote")
        target_datetime = time_instance.target_time.astimezone(pytz.timezone('Asia/Kolkata'))
        adjusted_target_datetime = target_datetime - timedelta(hours=5, minutes=30)
        current_datetime = timezone.now().astimezone(pytz.timezone('Asia/Kolkata'))

        if current_datetime >= adjusted_target_datetime:
            if request.method == 'POST':
                username = request.user.username
                password = request.POST.get('password')
                data = LoginKey.objects.get(user=username)

                if data.validity == 1:
                    salt = data.salt
                    stored_password = data.key
                    a = verify_key(password, salt, stored_password)
                    if a:
                        request.session['is_authenticated'] = True
                        data.validity = 0
                        data.save()
                        return redirect('vote')
                    else:
                        messages.error(request, "Incorrect Password")
                else:
                    messages.error(request, "Password expired")
        else:
            messages.error(request, f"You will be able to vote only on  {adjusted_target_datetime.strftime('%d-%m-%y %I:%M %p')}")

    except Time.DoesNotExist:
        messages.error(request, "Target time for voting has not been set.")
    
    return render(request, 'check_password.html')

@login_required(login_url='login')
def vote(request):
    if not request.session.get('is_authenticated'):
        return redirect('check_password')
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
        #fetching key of user
        voter=request.user.username
        username=request.user.username
        name=request.user.user_profile.vid.fname
        email=request.user.user_profile.vid.email
        uid=generate_log_id(username,name)
        key=Key.objects.get(uid=uid)
        vkey=VoteKey.objects.get(uid=uid)
        if vkey.key_validity == 1:
            vote_key=decrypt_aes(vkey.key,key.key).decode('utf-8')
            can=Candidate.objects.get(id=id)
        #completed fetching    
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
        
                
                if name in ['unknown_person', 'no_persons_found', 'unknown']:
                    print("Authorization failed")
                    messages.error(request,"Authorization failed")
                
                elif name==voter:
                    vote=Votes.objects.create(candidate=can,vote=vote_key)
                    vkey.key_validity=0
                    vkey.save()
                    send_status(email)
                    return redirect('home')
                else:
                    print("hello")
                    print(name)
                    messages.error(request,"Authorization failed")
                    return redirect('vote')
                
            except Exception as e:
                print(f"Error: {e}")
                messages.error(request,"Error occurred while recognizing the face.")

            finally:
                if os.path.exists(unknown_img_path):
                    os.remove(unknown_img_path)
        else:
            messages.error(request,"You are already voted")
    return redirect('vote')

def view_result(request):
    us=request.user.user_profile.vid
    cid=us.Constituency.id
    co=Constituency.objects.get(id=cid)
    
    if co.published==1:
        vote_data = Count.objects.filter(constituency=co)
        data = {}
        for count in vote_data:
            candidate_name = count.candidate.first_name + " " + count.candidate.last_name
            data[candidate_name] = {
                'votes': count.votes,
                'image': count.candidate.profile_image.url
            }
        context = {'data': data}

        max_votes = -1
        candidate_with_max_votes = None
        for c in vote_data:
            if c.votes > max_votes:
                max_votes = c.votes
                candidate_with_max_votes = c.candidate
        
        if candidate_with_max_votes:
            details = candidate_with_max_votes
            context['details'] = details
            
        total_voters=VoteKey.objects.count()
        voted_voters=VoteKey.objects.filter(key_validity=0).count()
        context['total_voters']=total_voters
        context['voted_voters']=voted_voters
        return render(request, 'view_result.html', context)
    else:
        return render(request,'not_found.html')