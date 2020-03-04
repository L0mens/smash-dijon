from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.db.models import Q
from django.db import IntegrityError

from infos import smashgg as smash
from infos import key as smashkey
from infos import elo as elosys, statistics
from infos import youtube
from .models import Competitor,Character,Elo,Saison,Tournament,Tournament_state, Vod, Vodplaylist, Matchs
from .forms import TounrmamentAddForm, ConnexionForm

import json
from math import *


def home(request):
    saisons_dijon = Saison.objects.filter(prefix="Dijon").order_by('-number')
    calculated = Tournament_state.objects.get(state="Calculé")
    compet_by_saison = {}
    nb_tn_by_saison = {}
    for saison in saisons_dijon:
        total_tn = Tournament.objects.filter(saison=saison, state=calculated).count()
        eligible = (total_tn/3)
        compet_by_saison[f"{saison.title}{saison.number}"] = Elo.objects.filter(saison=saison, nb_tournament__gte=eligible).order_by('elo').reverse()
        nb_tn_by_saison[f"{saison.title}{saison.number}"] = total_tn
    
    tn_coming = Tournament.objects.filter(date__gt=timezone.now()).order_by('date')
    tn_finish = Tournament.objects.filter(date__lt=timezone.now(), saison=saisons_dijon[0]).order_by('-date')[:3]
    return render(request, 'ranking/home.html', locals())


def redir_to_home(request):
    return redirect(home)

def register_user(request):
    # Tant que les inscriptions sont désactiver, laisser cette ligne !!!
    return render(request, 'ranking/login.html', locals())
    try:
        user = User.objects.create_user(request.POST["username"], request.POST["email"], request.POST["password"])
        login(request, user)  # nous connectons l'utilisateur
        return redirect(user_page)
    except IntegrityError as duplicate:
        error_log = {
            "already_exist" : "Le nom du compte existe déjà"
        }
        return render(request, 'ranking/login.html', locals())
    except :
        return redirect(connexion)

def user_page(request):
    if request.user:
        return render(request, 'ranking/profile.html', locals())
    else:
        return redirect(connexion)

def connexion(request):
    error_log = []
    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                return redirect(user_page)
            else: # sinon une erreur sera affichée
                error_log = {
                    "error_loggin_in" : "Utilisateur inconnu ou mauvais de mot de passe."
                }
    else:
        form = ConnexionForm()

    return render(request, 'ranking/login.html', locals())

def deconnexion(request):
    logout(request)
    return redirect(home)

def about(request):    
    return render(request, 'ranking/a_propos.html', locals())

def vod(request):
    all_tournaments = Tournament.objects.all().order_by('date').reverse()
    tn_with_vods = []

    for tournoi in all_tournaments:
        vods = Vod.objects.filter(tournament=tournoi)
        if vods:
            tn_with_vods.append(tournoi)

    return render(request, 'ranking/vod.html', locals())

def vod_by_tournament(request,tn_name_slug):
    try:
        tournament = Tournament.objects.get(slug=tn_name_slug)
        vods = Vod.objects.filter(tournament=tournament)
        if not vods:
            error = "Le tournoi demandé ne possède pas de VODs"
    except Tournament.DoesNotExist:
        error = "Le tournoi demandé n'existe pas"

    return render(request, 'ranking/vod_by_tn.html', locals())

@permission_required('ranking.add_tournament')
def tournament_manage(request):
    form = TounrmamentAddForm(request.POST or None)
    form_save = False
    if form.is_valid():
        data = form.cleaned_data
        form.save()
        form_save = True
    
    all_tournaments = Tournament.objects.all().order_by('date').reverse()
    
    return render(request, 'ranking/tn_manage.html', locals())

@permission_required('ranking.add_tournament')
def vods_manage(request):
    tournament_list = Tournament.objects.all().order_by('date').reverse()
    error_on_create_vod = {}
    if request.GET.get('playlist_id') and request.GET.get('tournament_id'):
        tournament_of_vod = Tournament.objects.get(id=request.GET.get('tournament_id'))
        playlist_name = request.GET.get('playlist_name', "")
        playlist_exist = Vodplaylist.objects.filter(youtube_id=request.GET.get('playlist_id'))
        if not playlist_exist:
            datas = (youtube.get_playlist_items(playlist_id=request.GET.get('playlist_id') , nb_result=32, session=request.session))
            if not datas: 
                succes = False
                error_message = "Erreur d'authentification"
                datas = {}

            if len(datas.get("items", 0)) > 0:
                play = Vodplaylist.objects.create(name=playlist_name, youtube_id=request.GET.get('playlist_id'))
            
            for vid_infos in datas['items']:
                video_url = f"https://youtu.be/{vid_infos['contentDetails']['videoId']}"
                video_id = vid_infos['contentDetails']['videoId']
                title = vid_infos['snippet']['title']
                vod,created = Vod.objects.get_or_create(video_url=video_url, id_watch_video=video_id, title=title, playlist=play, tournament=tournament_of_vod)
                if not created:
                    succes = False
                    error_message = "Erreurs sur certaines VODs"
                    error_on_create_vod[video_id] = title
            print(error_on_create_vod)
            if not error_on_create_vod:
                succes = True
        else:
            succes = False
            error_message = "La playlist existe déjà"
    return render(request, 'ranking/vod_manage.html', locals())

@csrf_exempt
def test_post(request):
    datapost = json.loads(request.body)
    dict_return = {}
    try:
        tn_bd = Tournament.objects.get(slug=datapost["tn_slug"])
    except Tournament.DoesNotExist:
        dict_return['error'] : "Le tournoi n'existe pas"
    tn_state_calc = Tournament_state.objects.get(state='Calculé')

    return JsonResponse({"test": "test"})


def revert_tournament(request):
    tn_slug = request.GET.get('tn_slug', '')
    dict_return = {}
    added = Tournament_state.objects.get(state="Ajouté")
    try:
        tn_found = Tournament.objects.get(slug=tn_slug)
        dict_return['tournament_name'] = tn_found.name
        matches = Matchs.objects.filter(tournament=tn_found)
        list_set_player = set()
        dict_return['nb_matches'] = len(matches)
        for match in matches :
            winner = match.winner
            looser = match.looser
            looser.elo -= match.elo_lose
            looser.nb_match_lose -= 1
            looser.save()
            # print(looser.competitor.name, looser.nb_match_lose)
            winner.elo -= match.elo_win
            winner.nb_match_win -= 1
            winner.save()
            list_set_player.add(winner.competitor.name)
            list_set_player.add(looser.competitor.name)

        for elo_player_name in list_set_player:            
            comp = Competitor.objects.get(name=elo_player_name)
            for saison in tn_found.saison.all():
                elo_player = Elo.objects.get(competitor=comp,saison=saison)
                elo_player.nb_tournament -= 1
                elo_player.save()

        matches.delete()
        dict_return['nb_player'] = len(list_set_player)
        dict_return['players'] = [x for x in list_set_player]
        tn_found.state = added
        tn_found.save()

    except Tournament.DoesNotExist:
        dict_return['error'] : "Le tournoi n'existe pas"
    
    
    return JsonResponse(dict_return)

def reset_state_tournament(request):
    datapost = json.loads(request.body)
    dict_return = {
        "slug" : datapost["tn_slug"],
        "state" : None,
        "error" : None
    }
    try:
        tn_bd = Tournament.objects.get(slug=datapost["tn_slug"])
        tn_state_calc = Tournament_state.objects.get(state='Ajouté')
        tn_bd.state = tn_state_calc
        tn_bd.save()
        dict_return['state'] = tn_state_calc.state
    except Tournament.DoesNotExist:
        dict_return['error'] : "Le tournoi n'existe pas"

    return JsonResponse(dict_return)
        

def update_with_smashgg(request):
    gg = smash.Smashgg(smashkey.key)
    #Tournament management
    datapost = json.loads(request.body)
    dict_return = {
        "slug" : datapost["tn_slug"],
        "event" : datapost["event"],
        "saison_ids" : datapost["saison"],
        "pseudo_inscrits" : [],
        "state" : None,
        "error" : None
    }
    try:
        tn_bd = Tournament.objects.get(slug=datapost["tn_slug"])
    except Tournament.DoesNotExist:
        dict_return['error'] : "Le tournoi n'existe pas"
    tn_state_calc = Tournament_state.objects.get(state='Calculé')

    

    if tn_bd.state.state != 'Calculé':

        tn = gg.get_tournament(datapost["tn_slug"],datapost["event"])
        inscription = []
        print(tn.slug)
        #Season management
        list_saison = []
        for id_saison in datapost["saison"]:
            try:
                saison = Saison.objects.get(id=id_saison)
            except Saison.DoesNotExist:
                try:
                    saison = Saison.objects.get(end__gt=timezone.now(), start__lt=timezone.now())
                except Saison.DoesNotExist:
                    saison = Saison.objects.all()[0]
            list_saison.append(saison)
        
        #Competitor list management
        for saison in list_saison:
            print(saison)
            for entr in tn.entrants:
                print(entr.team, entr.name)
                try:
                    already_competitor = Competitor.objects.get(name=entr.name)
                    if entr.team != already_competitor.tag and entr.team :
                        print(already_competitor.tag, " va etre remplace par ", entr.team)
                        already_competitor.tag = entr.team
                        already_competitor.save()
                    elif already_competitor and not entr.team : 
                        print(already_competitor.tag, " va etre effacé")
                        already_competitor.tag = None
                        already_competitor.save()
                    try:
                        comp_elo = Elo.objects.get(competitor=already_competitor, saison=saison)
                        comp_elo.nb_tournament = comp_elo.nb_tournament + 1 
                        comp_elo.save()
                    except Elo.DoesNotExist:                        
                        olds_elos = Elo.objects.filter(competitor=already_competitor)
                        new_elo = Elo(competitor=already_competitor, saison=saison, elo=1500, nb_tournament=1)
                        #Trouver les anciens persos
                        if olds_elos:
                            for old in olds_elos:
                                new_elo.main_char = old.main_char
                                new_elo.second_char = old.second_char
                                new_elo.third_char = old.third_char
                        print(f"Inscription de {new_elo.competitor} dans {saison.prefix} {saison.title} {saison.number} ")
                        new_elo.save()
                except Competitor.DoesNotExist:
                    new = Competitor(name=entr.name, tag=entr.team)
                    new.save()
                    new_elo = Elo(competitor=new, saison=saison, elo=1500, nb_tournament=1)
                    new_elo.save()
                    print(f"Inscription de {new_elo.competitor} dans {saison.prefix} {saison.title} {saison.number} ")
                    inscription.append(entr)

            #Elo management

            elo_system = elosys.Elo_Sytem()
            set_with_problem = []
            for match in tn.sets[0]['sorted_sets']:
                try:
                    print(match)
                    elo_win = Elo.objects.get(competitor=Competitor.objects.get(name=match.winner.name), saison=saison)
                    elo_lose = Elo.objects.get(competitor=Competitor.objects.get(name=match.looser.name), saison=saison)
                    modif = elo_system.calc(elo_win,elo_lose,match.fullRoundText)
                    new_match = Matchs(fullRoundText=match.fullRoundText, roundText=match.round,
                                        winner=elo_win, looser=elo_lose, elo_win=modif[0],
                                        elo_lose=modif[1], tournament=tn_bd, score=match.score,
                                        winner_elo_value_before=elo_win.elo, looser_elo_value_before=elo_lose.elo)
                    elo_win.elo = elo_win.elo + modif[0]
                    elo_lose.elo = elo_lose.elo + modif[1]
                    elo_win.nb_match_win = elo_win.nb_match_win + 1
                    elo_lose.nb_match_lose = elo_lose.nb_match_lose + 1
                    elo_win.save()
                    elo_lose.save()
                    # print(elo_win, elo_lose)
                    
                    new_match.save()
                    print(new_match)
                except :
                    print('error recording set')
                    set_with_problem.append(match)
            
            #Change tournament state
            tn_bd.state = tn_state_calc
            tn_bd.nb_players = tn.nb_entrant
            tn_bd.save()
            dict_return['state'] = tn_state_calc.state
    else:
        dict_return['error'] = "Le tournoi est déjà calculé"
    # TODO Entrant is not serializable
    # dict_return['pseudo_inscrits'] = inscription
    return JsonResponse(dict_return)

def player_info(request, player_name):
    last_saison = Saison.objects.filter(prefix="Dijon").order_by('-number')[:1]
    calculated = Tournament_state.objects.get(state="Calculé")
    competitor = get_object_or_404(Competitor, name=player_name)
    elo_player = Elo.objects.get(saison=last_saison, competitor=competitor)
    total_tn = Tournament.objects.filter(saison=last_saison, state=calculated).count()
    eligible = ceil(total_tn/3)
    elo_test = Elo.objects.get(saison=last_saison, competitor=competitor)
    matches = Matchs.objects.filter(Q(winner=elo_test) | Q(looser=elo_test)).order_by('-tournament__date')
    matches_loose = Matchs.objects.filter(looser=elo_test)
    worst_en = statistics.get_worst_enemie(matches_loose)
    return render(request, 'ranking/player_info.html', locals())

def player_list(request):
    calculated = Tournament_state.objects.get(state="Calculé")
    last_saison = Saison.objects.filter(prefix="Dijon").order_by('-number')[:1]
    elo_last_saison = Elo.objects.filter(saison=last_saison).order_by('elo').reverse()
    total_tn = Tournament.objects.filter(saison=last_saison, state=calculated).count()
    eligible = (total_tn/3)
            
    return render(request, 'ranking/player_list.html', locals())

def tournament_list(request):
    saisons_dijon = Saison.objects.filter(prefix="Dijon").order_by('-number')
    return render(request, 'ranking/tn_list.html', locals())

def oauth2callback(request):
    youtube.oauthcallback(request,request.session)
    return redirect(reverse('vodsmanage'))

def authorize(request):
    authorized_url = youtube.autorize(request)
    return redirect(authorized_url)

def test_youtube(request):
    dict_return = {}
    tn = Tournament.objects.get(slug="at-gaming-night-s2-8-1")
    all_matches = Matchs.objects.filter(tournament=tn)
    sma = smash.Smashgg("")
    list_m = []
    for match in all_matches:
        o_m = {
            "round" : match.roundText,
            "weight" : sma.get_index_of_sort_set(64,match.roundText),
            "tn" : match.tournament.name,
            "winner" : match.winner.competitor.name,
            "looser" : match.looser.competitor.name,
        }
        list_m.append(o_m)
    dict_return['list'] = list_m
    return JsonResponse(dict_return)

@permission_required('ranking.add_tournament')
def merge_elo(request):
    if request.method == "POST":
        try:
            elo_to = Elo.objects.get(pk=request.POST['elo_to'])
            elo_from = Elo.objects.get(pk=request.POST['elo_from'])
            matches = reversed(Matchs.objects.filter(Q(winner=elo_from) | Q(looser=elo_from)))
            elo_to.main_char = elo_from.main_char
            elo_to.main_char_skin = elo_from.main_char_skin
            elo_to.second_char = elo_from.second_char
            elo_to.second_char_skin = elo_from.second_char_skin
            elo_to.third_char = elo_from.third_char
            elo_to.third_char_skin = elo_from.third_char_skin
            for match in matches:
                if match.looser == elo_from:
                    elo_to.elo += match.elo_lose
                    match.looser = elo_to
                if match.winner == elo_from:
                    elo_to.elo += match.elo_win
                    match.winner = elo_to
                match.save()
            elo_to.save()
            elo_from.delete()
        except Elo.DoesNotExist:
            error = "Elo id's not matching"
    last_saison = Saison.objects.filter(prefix="Dijon").order_by('-number')[:1]
    elo_player_list = Elo.objects.filter(saison=last_saison)
    return render(request, 'ranking/merge_elo.html', locals())

def perso_select(request):
    last_saison = Saison.objects.filter(prefix="Dijon").order_by('-number')[:1]
    elo_player_list = Elo.objects.filter(saison=last_saison)
    chara_list = Character.objects.all().order_by('name_en')
    nb_skin_range = range(8)
    return render(request, 'ranking/characters.html', locals())

def stage_select(request):
    return render(request, 'ranking/stage.html', locals())

def discord_pr_player_info(request, player_name):
    last_saison = Saison.objects.filter(prefix="Dijon").order_by('-number')[:1]
    calculated = Tournament_state.objects.get(state="Calculé")
    
    try:
        competitor = Competitor.objects.get(name__iexact=player_name)
        elo_player = Elo.objects.get(saison=last_saison, competitor=competitor)
        total_tn = Tournament.objects.filter(saison=last_saison, state=calculated).count()
        eligible = ceil(total_tn/3)
        matches = Matchs.objects.filter(Q(winner=elo_player) | Q(looser=elo_player))[::-1][:10]
        list_matches = [{'match' : f"{match.winner.competitor.name} vs {match.looser.competitor.name}",
                         "score" : match.score}  for match in matches]
        matches_loose = Matchs.objects.filter(looser=elo_player)
        worst_en = statistics.get_worst_enemie(matches_loose)
        if elo_player.nb_tournament < eligible :
            is_eligible = False
        else:
            is_eligible = True

        all_elo_eligible = Elo.objects.filter(saison=last_saison, nb_tournament__gte= eligible).order_by('-elo')
        rank = -1
        for index,elo in enumerate(all_elo_eligible):
            if elo.competitor.name == competitor.name:
                rank = index+1
        list_char = []
        if elo_player.main_char:
            list_char.append(elo_player.main_char.name_fr)
        if elo_player.second_char:
            list_char.append(elo_player.second_char.name_fr)
        if elo_player.third_char:
            list_char.append(elo_player.third_char.name_fr)
        print(list_char)

        dict_return = {
            "player_name" : f"{competitor.name}",
            "player_tag" : f"{competitor.tag}",
            "player_full_name" : f"{competitor.__str__()}",
            "season" : f"{last_saison[0].prefix} {last_saison[0].title} {last_saison[0].number}",
            "elo_score" : elo_player.elo,
            "characters" : list_char,
            "stats" : {
                "nb_tournament" : elo_player.nb_tournament,
                "nb_win" : elo_player.nb_match_win,
                "nb_lose" : elo_player.nb_match_lose
            },
            "rank" : rank,
            "is_eligible": is_eligible,
            "records" : {
                "worst_enemie" : worst_en
            },
            "last_matches": list_matches
        }
        
    except Elo.DoesNotExist:
        dict_return = {
            "error" : "This player didn't exist, or he didn't play this season"
        }
    except Competitor.DoesNotExist:
        dict_return = {
            "error" : "This player didn't exist, or he didn't play this season"
        }
    
    return JsonResponse(dict_return)