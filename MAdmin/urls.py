from django.urls import path
from .import views
urlpatterns = [
    path('home',views.admin_home,name='ahome'),
    path('add_cadmin',views.add_cadmins,name='cadmins'),
    path('constituency',views.constituency,name='constituency'),
    path('delete/<pk>',views.delete_constituency,name='delete_c'),
    path('cwDetails/<pk>',views.view_admin,name='cwDetails'),
    path('display_candidates',views.display_candidates,name='display_candidates'),
    path('see_details/<pk>',views.see_details,name='see_details'),
    path('admin_view_result',views.admin_view_result,name='admin_view_result')
]