from django.db import models
from django.contrib.auth.models import User
from MAdmin.models import *

class CWadmin(models.Model):
    fname=models.CharField(max_length=30)
    lname=models.CharField(max_length=30)
    email=models.CharField(max_length=50)
    phone=models.CharField(max_length=12)
    user=models.OneToOneField(User,related_name='staff_profile',on_delete=models.CASCADE)
    image=models.ImageField(upload_to='media/',null=True)
    state=models.CharField(max_length=50)
    constituency=models.OneToOneField(Constituency,related_name='admin_constituency',on_delete=models.CASCADE)
    adharno=models.CharField(max_length=20,null=True)
    cp=models.IntegerField(null=True,default=0)
    
    def __str__(self):
        return self.constituency.name
    
class Candidate(models.Model):
    #personal details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone=models.CharField(max_length=12)
    email=models.CharField(max_length=30)
    adharNo=models.CharField(max_length=12,null=False)
    hname=models.CharField(max_length=100)
    pincode=models.CharField(max_length=10)
    state=models.CharField(max_length=30)
    district=models.CharField(max_length=30)
    taluk=models.CharField(max_length=30)
    village=models.CharField(max_length=30)
    #participation information
    p_constituency = models.ForeignKey(Constituency,related_name='ca_co',on_delete=models.CASCADE)
    p_state=models.CharField(max_length=30)
    profile_image = models.ImageField(upload_to='media/candidates/')
    symbol=models.ImageField(upload_to='media/symbol/')
    part_afiliation=models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.p_constituency}"

    
class Control(models.Model):
    key=models.CharField(max_length=20)
    counted=models.IntegerField(default=0)
    
class Count(models.Model):
    constituency=models.ForeignKey(Constituency,related_name='candudate_constituency',on_delete=models.DO_NOTHING,null=True)
    candidate=models.ForeignKey(Candidate,related_name='candidate_data',on_delete=models.CASCADE)
    votes=models.IntegerField(default=0)
    
    
    
    
    
