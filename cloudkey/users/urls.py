from django.urls import path
from . import views

urlpatterns = [
    path('profile', views.profile_view, name='profile'),
    path('reg_form', views.reg_user, name='reg'),
    path('add_card', views.add_new_card, name='add_card'),
]
