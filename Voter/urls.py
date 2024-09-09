from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('login',views.user_login,name='login'),
    path('logout',views.logout_user,name='logout'),
    path('vote',views.vote,name='vote'),
    path('help',views.help,name='help'),
    path('validate_user_otp',views.otp_page,name='validate_user_otp'),
    path('details/<int:id>/',views.details,name='details'),
    path('detailsOfcandidates',views.display_candiadtes,name='det_of_cand'),
    path('candidate_details/<int:pk>',views.candidate_details,name='candidate_details'),
    path('check_password',views.check_password,name='check_password'),
    path('voting/<int:id>',views.cast_vote,name='cast_vote')
]