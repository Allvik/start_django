from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registration', views.registration),
    path('login', views.login),
    path('yourCabinet', views.getCabinet),
    path('debug_base', views.debug_base),
    path('clear_bases', views.clear_bases)
]
