from django.urls import path
from .import views

urlpatterns = [
    path('cwhome',views.cwadminHome,name='cwhome'),
    path('AddCandiadte',views.add_candidates,name='add_candidates'),
    path('changePassword',views.change_password,name='change_password'),
    path('validate',views.validate,name='validate_otp'),
    path('candidates',views.display_candidates,name='candidates'),
    path('update/<pk>',views.update_candidates,name='update_c')
]