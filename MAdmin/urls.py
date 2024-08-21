from django.urls import path
from .import views
urlpatterns = [
    path('home',views.admin_home,name='ahome'),
    path('add_cadmin',views.add_cadmins,name='cadmins'),
    path('constituency',views.constituency,name='constituency'),
    path('delete/<pk>',views.delete_constituency,name='delete_c')
]