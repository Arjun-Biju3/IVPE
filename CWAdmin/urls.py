from django.urls import path
from .import views

urlpatterns = [
    path('cwhome',views.cwadminHome,name='cwhome')
]