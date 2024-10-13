from django.shortcuts import render,redirect
from CWAdmin.models import *
from MAdmin.models import *
from django.contrib.auth.models import User
from MAdmin.password import *
from django.contrib import messages
import os
from django.conf import settings
from Voter.models import *

def admin_home(request):
    return render(request,'index2.html')


def add_cadmins(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        state = request.POST.get('state')
        constituency_id = request.POST.get('constituency')
        image = request.FILES.get('image')
        adno=request.POST.get('adno')
        password = generate_simple_password()

        try:
            constituency = Constituency.objects.get(id=constituency_id)
            user = User.objects.create_user(username=email, password=password, is_staff=True)
            CWadmin.objects.create(
                fname=fname,
                lname=lname,
                email=email,
                phone=phone,
                state=state,
                user=user,
                adharno=adno,
                constituency=constituency,
                image=image
            )
            constituency.admin_assigned=1
            constituency.save()
            send_mail(email, email, password, fname)
            return redirect('cadmins')
        except Constituency.DoesNotExist:
            messages.error(request, "Selected constituency does not exist.")
        except Exception as e:
            if User.objects.filter(username=email).exists():
                User.objects.get(username=email).delete()
            messages.error(request,"An error occurred")

    constituencies = Constituency.objects.filter(admin_assigned=0)
    admins=CWadmin.objects.all()
    context = {'constituencies': constituencies,'admin':admins}
    
    return render(request, 'add_admins.html', context)


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

def view_admin(request,pk):
    if request.POST and 'update' in request.POST:
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        state = request.POST.get('state')
        image = request.FILES.get('image')
        adno=request.POST.get('adno')
        image = request.FILES.get('image')
        edit=CWadmin.objects.get(id=pk)
        #update
        edit.fname=fname
        edit.lname=lname
        edit.email=email
        edit.phone=phone
        edit.state=state
        edit.adharno=adno
        if image != None:
            image_path = os.path.join(settings.MEDIA_ROOT, str(edit.image))
            if os.path.exists(image_path):
                os.remove(image_path)
            edit.image=image
        edit.save()
        return redirect('cadmins')
    if request.POST and 'delete' in request.POST:
        email=request.POST.get('email')
        val=CWadmin.objects.get(id=pk)
        user = val.user
        ctcy=Constituency.objects.get(name=val.constituency)
        val.delete()
        user.delete()
        ctcy.admin_assigned=0
        val2=User.objects.get(id=1)
        return redirect('cadmins')
    c=CWadmin.objects.get(id=pk)
    context={'c':c}
    return render(request,'details_cwadmin.html',context)

def display_candidates(request):
    can=Candidate.objects.all()
    context={'candidates':can}
    return render(request,'admin_display_candidates.html',context)

def see_details(request,pk):
    can=Candidate.objects.get(id=pk)
    context={'candidate':can}
    return render(request,'see_details.html',context)


def admin_view_result(request):
    co = Constituency.objects.all()
    selected_constituency = None
    vote_data = []
    
    if request.method == 'POST':
        constituency_id = request.POST.get('constituency')
        if constituency_id:
            selected_constituency = Constituency.objects.get(id=constituency_id)
            vote_data = Count.objects.filter(constituency=constituency_id)
    data = {}
    for count in vote_data:
        candidate_name = count.candidate.first_name + " " + count.candidate.last_name
        data[candidate_name] = {
            'votes': count.votes,
            'image': count.candidate.profile_image.url
        }
    context = {
        'constituencies': co,
        'data': data,
        'selected_constituency': selected_constituency
    }

    # Finding the candidate with the maximum votes
    max_votes = -1
    candidate_with_max_votes = None
    for c in vote_data:
        if c.votes > max_votes:
            max_votes = c.votes
            candidate_with_max_votes = c.candidate

    if candidate_with_max_votes:
        context['details'] = candidate_with_max_votes

    # Voting statistics
    total_voters = VoteKey.objects.count()
    voted_voters = VoteKey.objects.filter(key_validity=0).count()
    toatl_c_voters=VoterList.objects.filter(Constituency=selected_constituency).count()
    context['total_voters'] = total_voters
    context['voted_voters'] = voted_voters
    context['toatl_c_voters']=toatl_c_voters
    
    # Submission button state
    if selected_constituency:
        btn_display = selected_constituency.published
        context['submission_status'] = btn_display

    if request.POST and 'publish' in request.POST:
        id=request.POST.get('cid')
        print(id)
        co=Constituency.objects.get(id=id)
        co.published=1
        co.save()
    if request.POST and 'revoke' in request.POST:
        id=request.POST.get('cid')
        print(id)
        co=Constituency.objects.get(id=id)
        co.published=0
        co.save()

    return render(request, 'admin_view_result.html', context)
