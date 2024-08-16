from django.db import models
from django.contrib.auth.models import User

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
    constituency=models.CharField(max_length=30,null=True)
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
    key=models.TextField(max_length=70)
    salt=models.TextField(max_length=40)
    
    