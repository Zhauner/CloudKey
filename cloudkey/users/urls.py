from django.urls import path
from . import views

urlpatterns = [
    path('profile', views.profile_view, name='profile'),
    path('reg_form', views.reg_user, name='reg'),
]
