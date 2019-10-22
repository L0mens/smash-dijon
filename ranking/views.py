from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

from infos import smashgg as smash
from infos import key as smashkey
from infos import elo as elosys
from infos import youtube
from .models import Competitor,Elo,Saison,Tournament,Tournament_state, Vod, Vodplaylist
from .forms import TounrmamentAddForm, ConnexionForm

import json

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
    tn_finish = Tournament.objects.filter(date__lt=timezone.now(), saison=saisons_dijon[0]).order_by('-date')
    return render(request, 'ranking/home.html', locals())


def redir_to_home(request):
    return redirect(home)

def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
            else: # sinon une erreur sera affichée
                error = True
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
    vods_by_tournament = {}

    for tournoi in all_tournaments:
        vods = Vod.objects.filter(tournament=tournoi)
        if vods:
            vods_by_tournament[tournoi.name] = vods

    return render(request, 'ranking/vod.html', locals())

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
        #TODO Gérer l'OAuth 2.0 pour éviter le prompt dans la console
        playlist_exist = Vodplaylist.objects.filter(youtube_id=request.GET.get('playlist_id'))
        if not playlist_exist:
            datas = (youtube.get_playlist_items(playlist_id=request.GET.get('playlist_id') , nb_result=32, session=request.session))
            if len(datas.get("items", 0)) > 0:
                play = Vodplaylist.objects.create(name=playlist_name, youtube_id=request.GET.get('playlist_id'))
            
            for vid_infos in datas['items']:
                video_url = f"https://youtu.be/{vid_infos['contentDetails']['videoId']}"
                video_id = vid_infos['contentDetails']['videoId']
                title = vid_infos['snippet']['title']
                vod,created = Vod.objects.get_or_create(video_url=video_url, id_watch_video=video_id, title=title, playlist=play, tournament=tournament_of_vod)
                if not created:
                    error_on_create_vod[video_id] = title
            if not error_on_create_vod:
                succes = True
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
                    print(elo_win, elo_lose)
                    modif = elo_system.calc(elo_win,elo_lose,match.fullRoundText)
                    elo_win.elo = elo_win.elo + modif[0]
                    elo_lose.elo = elo_lose.elo + modif[1]
                    elo_win.nb_match_win = elo_win.nb_match_win + 1
                    elo_lose.nb_match_lose = elo_lose.nb_match_lose + 1
                    elo_win.save()
                    elo_lose.save()
                except :
                    print('error recording set')
                    set_with_problem.append(match)
            
            #Change tournament state
            tn_bd.state = tn_state_calc
            tn_bd.save()
            dict_return['state'] = tn_state_calc.state
    else:
        dict_return['error'] = "Le tournoi est déjà calculé"
    # TODO Entrant is not serializable
    # dict_return['pseudo_inscrits'] = inscription
    return JsonResponse(dict_return)


def oauth2callback(request):
    youtube.oauthcallback(request,request.session)
    return redirect(reverse('test'))

def authorize(request):
    authorized_url = youtube.autorize(request.session)
    return redirect(authorized_url)

def test_youtube(request):
    return render(request, 'ranking/test_ytb.html', locals())