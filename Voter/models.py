from django.db import models
from django.contrib.auth.models import User
from MAdmin.models import Constituency
from CWAdmin.models import *

class VoterList(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICES=((LIVE,'Live'),(DELETE,'Delete'))
    YES=1
    NO=0
    registered=((YES,'yes'),(NO,'no'))
    eligibility=((YES,'yes'),(NO,'no'))
    adharNo=models.CharField(max_length=12,null=False,primary_key=True)
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    dob=models.DateField()
    phone=models.CharField(max_length=10,null=False)
    email=models.CharField(max_length=50,null=False)
    hname=models.CharField(max_length=100)
    pincode=models.CharField(max_length=10)
    state=models.CharField(max_length=30)
    district=models.CharField(max_length=30)
    Constituency=models.ForeignKey(Constituency,related_name='con_vot',on_delete=models.CASCADE)
    taluk=models.CharField(max_length=30)
    village=models.CharField(max_length=30)
    delete_status=models.IntegerField(choices=DELETE_CHOICES,default=LIVE)
    register_status=models.IntegerField(choices=registered,default=NO)
    eligibility_status=models.IntegerField(choices=eligibility,default=YES)
    
    
    def __str__(self):
        return self.adharNo
    
class Profile(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICES=((LIVE,'Live'),(DELETE,'Delete'))
    delete_status=models.IntegerField(choices=DELETE_CHOICES,default=LIVE)
    user=models.OneToOneField(User,related_name='user_profile',on_delete=models.CASCADE)
    vid=models.OneToOneField(VoterList,related_name='user_details',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.user.username
    
class LoginKey(models.Model):
    user=models.CharField(max_length=20)
    key=models.TextField()
    salt=models.BinaryField()
    
class VoteKey(models.Model):
    uid=models.CharField(max_length=10)
    key=models.TextField()
    

class Votes(models.Model):
    candidate=models.ForeignKey(Candidate,related_name='candidate_profile',on_delete=models.CASCADE)  
    vote=models.ForeignKey(VoteKey,on_delete=models.DO_NOTHING)
    voted_at=models.DateTimeField(auto_now_add=True)
      
    
    