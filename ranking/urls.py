from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('calculate-tournament', views.update_with_smashgg, name='calculate-tournament'),
    path('reset-tournament', views.reset_state_tournament, name='reset-tournament'),
    path('tournaments', views.tournament_manage, name='tnmanage'),
    path('vods-admin', views.vods_manage, name='vodsmanage'),
    path('login', views.connexion, name='login'),
    path('logout', views.deconnexion, name='logout'),
    path('about', views.about, name='about'),
    path('vod', views.vod, name='vod'),
    path('test', views.test_post, name='test'),
]