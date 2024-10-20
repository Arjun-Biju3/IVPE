from django.shortcuts import render,redirect
from django.contrib import messages
from CWAdmin.otp import *
import re
from django.contrib.auth import authenticate,login,logout
from CWAdmin.models import *
import os
from django.conf import settings
from Voter.models import *
from Voter.key import *
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import pytz

def is_password_secure(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character."

    return True, "Password is secure."


def cwadminHome(request):
    return render(request,'index3.html')

def add_candidates(request):
    if request.method == 'POST':
        constituency=request.user.staff_profile.constituency
        Candidate.objects.create(
            first_name=request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            age = request.POST.get('age'),
            phone = request.POST.get('phone'),
            email = request.POST.get('email'),
            adharNo = request.POST.get('adharNo'),
            hname = request.POST.get('hname'),
            state = request.POST.get('state'),
            district = request.POST.get('district'),
            taluk = request.POST.get('taluk'),
            village = request.POST.get('village'),
            pincode = request.POST.get('pincode'),
            p_state=constituency.state,
            p_constituency=constituency,
            part_afiliation = request.POST.get('part_afiliation'),
            profile_image = request.FILES.get('profile_image'),
            symbol = request.FILES.get('symbol'))
        messages.success(request,"Candidate added succesfilly")
        return redirect('add_candidates')
    return render(request,'add_candidates.html')

def change_password(request):
    if request.POST:
        password=request.POST.get('old')
        new=request.POST.get('new')
        c_new=request.POST.get('cnew')
        if request.user.check_password(password):
            if new==password:
                error_message="New password should not be same as old"
                messages.error(request,error_message)
            else:
                if new==c_new:
                    is_secure, message = is_password_secure(new)
                    if is_secure:
                        email=request.user.staff_profile.email
                        request.session['password']=new
                        #generate otp
                        otp=generate_otp()
                        request.session['email']=email
                        request.session['otp']=otp
                        request.session['otp_expires'] = (datetime.now() + timedelta(minutes=5)).isoformat()
                        #send mail           
                        send_email(email,otp)
                        print(otp)
                        return redirect('validate_otp')
                    else:
                        messages.error(request,message)
                else:
                    error_message="Passwords are not matching"
                    messages.error(request,error_message)
        else:
            error_message="Enter a valid password"
            messages.error(request,error_message)
            
    return render(request,'change_password.html')
    
def validate(request):
    success_message="OTP has been send succesfully"
    messages.success(request,success_message)
    if request.POST:
        otp=request.POST.get('otp')
        res=validate_otp(request,otp)
        if res==1:
            password=request.session.get('password')
            request.user.set_password(password)
            request.user.save()
            clear_otp(request)
            request.user.staff_profile.cp=1
            request.user.staff_profile.save()
            logout(request)
            message="Password changed Succesfully.Login to continue"
            request.session['c']=1
            messages.success(request,message)
            return redirect('login')
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
    return render(request,'validate.html')

def display_candidates(request):
    candidate=Candidate.objects.filter(p_constituency=request.user.staff_profile.constituency)
    context={'candidates':candidate}
    return render(request,'display_candidate.html',context)

def update_candidates(request,pk):
    if request.POST and 'update' in request.POST:
        first_name=request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        adharNo = request.POST.get('adharNo')
        hname = request.POST.get('hname')
        state = request.POST.get('state')
        district = request.POST.get('district')
        taluk = request.POST.get('taluk')
        village = request.POST.get('village')
        pincode = request.POST.get('pincode')
        part_afiliation = request.POST.get('part_afiliation')
        profile_image = request.FILES.get('profile_image')
        symbol = request.FILES.get('symbol')
        can=Candidate.objects.get(id=pk)
        #update
        can.first_name=first_name
        can.last_name=last_name
        can.age=age
        can.phone=phone
        can.email=email
        can.adharNo=adharNo
        can.hname=hname
        can.state=state
        can.district=district
        can.taluk=taluk
        can.village=village
        can.pincode=pincode
        can.part_afiliation=part_afiliation
        if profile_image != None:
            image_path = os.path.join(settings.MEDIA_ROOT, str(can.profile_image))
            if os.path.exists(image_path):
                os.remove(image_path)
            can.profile_image=profile_image
        if symbol != None:
            image_path = os.path.join(settings.MEDIA_ROOT, str(can.symbol))
            if os.path.exists(image_path):
                os.remove(image_path)
            can.symbol=symbol
        can.save()
        return redirect('candidates')
    if request.POST and 'delete' in request.POST:
        can=Candidate.objects.get(id=pk)
        can.delete()
        return redirect('candidates')
    candidate=Candidate.objects.get(id=pk)
    context={'c':candidate}
    return render(request,'edit_candidates.html',context)


def detailed_result(request):
    c=request.user.staff_profile.constituency
    co=Constituency.objects.get(id=c.id)
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
    
    if request.POST and 'publish' in request.POST:
        co.submitted=1
        co.save()
    if request.POST and 'revoke' in request.POST:
        co.submitted=0
        co.save()
    btn_display=co.submitted
    context['submission_status']=btn_display
    return render(request, 'detailed_result.html', context)


def result(request):
    c=request.user.staff_profile.constituency
    co=Constituency.objects.get(id=c.id)
    try:
        time_instance = Time.objects.get(key="start_count")
        time_instance_two=Time.objects.get(key="end_count")
        target_datetime = time_instance.target_time.astimezone(pytz.timezone('Asia/Kolkata'))
        adjusted_target_datetime = target_datetime - timedelta(hours=5, minutes=30)
        current_datetime = timezone.now().astimezone(pytz.timezone('Asia/Kolkata'))
        ending_date_time=time_instance_two.target_time.astimezone(pytz.timezone('Asia/Kolkata'))
        adjusted_end_time=ending_date_time - timedelta(hours=5,minutes=30)
        
        if current_datetime > adjusted_end_time:
            messages.error(request, "Counting Completed")
        else:
            #
            if current_datetime >= adjusted_target_datetime:
                if request.POST and 'count' in request.POST:
                    constituency=request.user.staff_profile.constituency
                    can=Candidate.objects.filter(p_constituency=constituency)
                    
                    
                    for candidate in can:
                    
                        vote_count = 0
                        v=Votes.objects.filter(candidate=candidate)
                        for i in v:
                            id=get_left_part(i.vote) #fetching id of key
                            try:
                                v = VoteKey.objects.get(uid=id)
                                key=Key.objects.get(uid=id)
                                vote_key=decrypt_aes(v.key,key.key).decode('utf-8')
                                if vote_key==i.vote:
                                    vote_count += 1
                            except VoteKey.DoesNotExist:
                                pass
                        data, created = Count.objects.get_or_create(candidate=candidate)
                        data.constituency=co
                        data.votes = vote_count  
                        data.save()
                        
                        co.counted=1
                        co.save()
            else:
                messages.error(request, f"You will be able to count only after  {adjusted_target_datetime.strftime('%d-%m-%y %I:%M %p')}")
            #
    except Time.DoesNotExist:
        messages.error(request, "Target time for counting has not been set.")
   
    if co.counted == 1:
        return redirect('detailed_result')
    return render(request,'result.html')



    