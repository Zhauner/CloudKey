from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('bot', views.bot_info, name='botinfo'),
]
