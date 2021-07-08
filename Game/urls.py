from . import views
from django.urls import path

urlpatterns = [
    path('createGame', views.createGame),
    path('enterGame', views.enterGame),
    path('play', views.play),
    path('makeWords', views.makeWords)
]
