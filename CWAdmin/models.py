from django.db import models
from django.contrib.auth.models import User
from MAdmin.models import *

class CWadmin(models.Model):
    fname=models.CharField(max_length=30)
    lname=models.CharField(max_length=30)
    email=models.CharField(max_length=50)
    phone=models.CharField(max_length=10)
    user=models.OneToOneField(User,related_name='staff_profile',on_delete=models.CASCADE)
    image=models.ImageField(upload_to='media/',null=True)
    state=models.CharField(max_length=50)
    constituency=models.OneToOneField(Constituency,related_name='admin_constituency',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.email
    
    
