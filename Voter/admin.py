from django.contrib import admin
from Voter.models import VoterList,Profile,LoginKey

admin.site.register(VoterList)
admin.site.register(Profile)
admin.site.register(LoginKey)
