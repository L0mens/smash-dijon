from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('calculate-tournament', views.update_with_smashgg, name='calculate-tournament'),
    path('reset-tournament', views.reset_state_tournament, name='reset-tournament'),
    path('revert-tournament', views.revert_tournament, name='revert-tournament'),
    path('tournaments-manage', views.tournament_manage, name='tnmanage'),
    path('vods-admin', views.vods_manage, name='vodsmanage'),
    path('saison-scale', views.next_saison_rescale, name='saisonscale'),
    path('register', views.register_user, name='register_user'),
    path('login', views.connexion, name='login'),
    path('logout', views.deconnexion, name='logout'),
    path('profile', views.user_page, name='profile'),
    path('about', views.about, name='about'),
    path('stream', views.stream, name='stream'),
    path('characters', views.perso_select, name='perso_select'),
    path('characters/save', views.perso_save, name='perso_save'),
    path('stage', views.stage_select, name='stage_select'),
    path('roa', views.roa_main, name='roa'),
    path('vod', views.vod, name='vod'),
    path('vod/<str:tn_name_slug>', views.vod_by_tournament, name='vod_by_tn'),
    path('test', views.test_youtube, name='test'),
    path('tournaments', views.tournament_list, name='tnlist'),
    path('players', views.player_list_choose_saison, name='playerlist'),
    path('players/<str:saison_str>', views.player_list_by_saison, name='playerlistbysaison'),
    path('players/stats/<str:saison_str>/<str:player_name>', views.player_info, name='playerinfo'),
    path('authorize', views.authorize, name='authorize'),
    path('oauth2callback', views.oauth2callback, name='oauth'),
    path('elo-merge', views.merge_elo, name='elomerge'),
    path('api/players/<str:player_name>', views.discord_pr_player_info, name='disc_pl_info'),
]