from . import views
from django.urls import path

urlpatterns = [
    path('createGame', views.createGame),
    path('enterGame', views.enterGame),
    path('play', views.play),
    path('makeWords', views.makeWords),
    path('start_round', views.start_round),
    path('no', views.noWord),
    path('yes', views.yesWord),
    path('standings', views.getStandings)
]
