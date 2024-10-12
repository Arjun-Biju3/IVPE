from django.db import models

class Constituency(models.Model):
    state=models.CharField(max_length=30)
    name=models.CharField(max_length=30)
    admin_assigned=models.IntegerField(default=0)
    counted=models.IntegerField(default=0)
    submitted=models.IntegerField(default=0)
    published=models.IntegerField(default=0)
    def __str__(self):
        return self.name