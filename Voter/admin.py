from django.contrib import admin
from Voter.models import VoterList,Profile,LoginKey,VoteKey,Key

admin.site.register(VoterList)
admin.site.register(Profile)
admin.site.register(LoginKey)
admin.site.register(VoteKey)
admin.site.register(Key)
