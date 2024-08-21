from django.db import models

class Constituency(models.Model):
    state=models.CharField(max_length=30)
    name=models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
    
