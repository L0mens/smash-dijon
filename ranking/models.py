from django.db import models
from django.contrib.auth.models import User
from datetime import datetime   
# Create your models here.

class Competitor(models.Model):
    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=255, null=True, blank=True, default="")

    def __str__(self):
        if self.tag:
            return f"{self.tag} | {self.name}"
        else:
            return f"{self.name}"


class Saison(models.Model):
    start = models.DateTimeField(verbose_name="Début de la saison")
    end = models.DateTimeField(verbose_name="Fin de la saison")
    title = models.CharField(max_length=255 , default='Saison')
    prefix = models.CharField(max_length=255, default='Dijon')
    number = models.IntegerField()
    competitor = models.ManyToManyField(Competitor, through='Elo')
    annee_de_jeu = models.IntegerField(default=2)
    eligibilty_percent = models.IntegerField(default=33)
    split_name = models.CharField(max_length=255, default="", blank=True,null=True)
    split_number = models.IntegerField(null=True)
    next_saison = models.ForeignKey('Saison', on_delete=models.CASCADE, blank=True, null=True, related_name="prochaine_saison")
    previous_saison = models.ForeignKey('Saison', on_delete=models.CASCADE, blank=True, null=True, related_name="precedante_saison")
    is_main_saison = models.BooleanField(default=False, verbose_name="Saison Principale")
    hidden =  models.BooleanField(default=False, verbose_name="Cacher la saison")

    def __str__(self):
        return f"{self.id}|| {self.prefix} / {self.title} {self.number} / {self.split_name} ({self.start} => {self.end})"

class Elo(models.Model):
    elo = models.IntegerField()
    elo_initial = models.IntegerField(default=1400)
    nb_tournament = models.IntegerField(default=0)
    nb_match_win = models.IntegerField(default=0)
    nb_match_lose = models.IntegerField(default=0)
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE)
    main_char = models.ForeignKey('Character', on_delete=models.CASCADE,blank=True, null=True, related_name='main_char')
    main_char_skin = models.IntegerField(default=0)
    second_char = models.ForeignKey('Character', on_delete=models.CASCADE,blank=True, null=True, related_name='second_char')
    second_char_skin = models.IntegerField(default=0)
    third_char = models.ForeignKey('Character', on_delete=models.CASCADE,blank=True, null=True, related_name='third_char')
    third_char_skin = models.IntegerField(default=0)
    is_away = models.BooleanField(default=False, verbose_name="Ne participe plus")
    saison = models.ForeignKey(Saison, on_delete=models.CASCADE)
    def __str__(self):
        return f"({self.saison.prefix} {self.saison.title} {self.saison.number})   {self.competitor} : {self.elo}"

class Tournament(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    event = models.CharField(max_length=255)
    event_slug = models.CharField(max_length=255, null=True)
    state = models.ForeignKey('Tournament_state', on_delete=models.CASCADE)
    serie = models.ForeignKey('Tournament_serie', on_delete=models.CASCADE, null=True, blank=True)
    saison = models.ManyToManyField(Saison, related_name='Saison')
    place = models.ForeignKey('Tournament_place', on_delete=models.CASCADE, null=True, blank=True)
    association = models.ForeignKey('Association', on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now, blank=True)
    nb_players = models.IntegerField(default=0)
    weight = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class Tournament_state(models.Model):
    state = models.CharField(max_length=255)
    def __str__(self):
        return self.state

class Tournament_serie(models.Model):
    name = models.CharField(max_length=255)
    logo_url = models.URLField(default="", null=True, blank=True)
    city = models.ForeignKey('City', on_delete=models.CASCADE, null=True, blank=True)
    is_on_pr = models.BooleanField(default=True, verbose_name="Possède des tournois du Power Ranking")
    def __str__(self):
        return self.name

class Tournament_place(models.Model):
    name = models.CharField(max_length=255)
    logo_url = models.URLField(default="", null=True, blank=True)
    adress = models.CharField(max_length=255)
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class City(models.Model):
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.name

class Association(models.Model):
    name = models.CharField(max_length=255)
    logo_url = models.URLField(default="", null=True)
    site_url = models.URLField(default="", null=True)
    def __str__(self):
        return self.name

class Matchs(models.Model):
    fullRoundText = models.CharField(max_length=255, null=True, blank=True)
    roundText = models.CharField(max_length=255, null=True, blank=True)
    winner = models.ForeignKey('Elo', on_delete=models.CASCADE, related_name='winner')
    looser = models.ForeignKey('Elo', on_delete=models.CASCADE, related_name='looser')
    elo_win = models.IntegerField(default=0)
    elo_lose = models.IntegerField(default=0)
    winner_elo_value_before = models.IntegerField(default=0)
    looser_elo_value_before = models.IntegerField(default=0)
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
    score = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return f"{self.tournament.name} / {self.roundText} / {self.winner.competitor.name} +{self.elo_win} vs {self.looser.competitor.name} {self.elo_lose} {self.score}"

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # La liaison OneToOne vers le modèle User
    competitor = models.OneToOneField(Competitor, on_delete=models.CASCADE, null=True, related_name='nom_smash')

    def __str__(self):
        return "Profil de {0}".format(self.user.username)

class Character(models.Model):
    name_fr = models.CharField(max_length=255, unique=True)
    name_en = models.CharField(max_length=255)
    icon_static = models.CharField(max_length=255)
    splash_url = models.URLField(default="", null=True, blank=True)
    def __str__(self):
        return f"{self.name_fr}"

class Vod(models.Model):
    video_url = models.URLField(default="", null=True)
    id_watch_video = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    playlist = models.ForeignKey('Vodplaylist', on_delete=models.CASCADE, null=True)
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
    # player_one = models.ForeignKey('Elo', on_delete=models.SET_NULL, null=True, related_name="player_one")
    # player_two = models.ForeignKey('Elo', on_delete=models.SET_NULL, null=True, related_name="player_two")
    def __str__(self):
        return f"{self.title}"

class Vodplaylist(models.Model):
    youtube_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, default="")
    def __str__(self):
        return f"{self.youtube_id} {self.name}"

class MessageInfo(models.Model):
    STATUS_CHOICE = [("active", "Active"), ("archive", "Archiver")]
    TYPE_CHOICE = [("info", "Information"), ("warning", "Attention"), ("error", "Erreur")]
    text = models.CharField(max_length=255, default="")
    status = models.CharField(max_length=255, choices=STATUS_CHOICE)
    message_type = models.CharField(max_length=255, choices=TYPE_CHOICE)

    def __str__(self):
        return f"({self.status} | {self.message_type}) {self.text}"

class SiteOptions(models.Model):
    option_name = models.CharField(max_length=255)
    is_option_active = models.BooleanField(default=False, verbose_name="Système Actif")
    is_inscription_open = models.BooleanField(default=False, verbose_name="Inscriptions Ouverte")
    
    def __str__(self):
        return f"{self.option_name} | Active : {self.is_option_active}"
