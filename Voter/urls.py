from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('login',views.user_login,name='login'),
    path('logout',views.logout_user,name='logout'),
    path('vote',views.vote,name='vote'),
    path('candidates',views.candidates,name='candidates'),
    path('help',views.help,name='help'),
    path('validate',views.otp_page,name='validate'),
    path('details/<int:id>/',views.details,name='details')
]