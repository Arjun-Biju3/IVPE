from django.db import models

class Constituency(models.Model):
    state=models.CharField(max_length=30)
    name=models.CharField(max_length=30)
    admin_assigned=models.IntegerField(default=0)
    counted=models.IntegerField(default=0)
    submitted=models.IntegerField(default=0)
    published=models.IntegerField(default=0)
    district = models.CharField(max_length=100,null=True) 
    taluk = models.CharField(max_length=100, blank=True, null=True) 
    village_town = models.CharField(max_length=100, blank=True, null=True)  
    total_population = models.IntegerField(null=True)  
    eligible_voters = models.IntegerField(null=True) 
    urban_rural_ratio = models.CharField(max_length=50, blank=True, null=True)  
    geographical_area = models.DecimalField(max_digits=10, decimal_places=2,null=True) 
    boundaries = models.TextField(blank=True, null=True)  
    voter_turnout = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True) 
    
    def __str__(self):
        return self.name
    
class Time(models.Model):
    key=models.CharField(max_length=20)
    target_time = models.DateTimeField(null=True)



   
