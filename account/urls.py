from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('profile/',views.profile_view,name='profile'),
    path('get-category/',views.display_category),
    path('update-address/',views.update_address,name='update_address'),
    ]