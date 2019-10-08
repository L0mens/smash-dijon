from django.db import models
from django.contrib.auth.models import User
from datetime import datetime   
# Create your models here.

class Competitor(models.Model):
    name = models.CharField(max_length=42)
    tag = models.CharField(max_length=10, null=True)

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

    def __str__(self):
        return f"{self.id}|| {self.prefix} / {self.title} {self.number} ({self.start} => {self.end})"

class Elo(models.Model):
    elo = models.IntegerField()
    nb_tournament = models.IntegerField(default=0)
    nb_match_win = models.IntegerField(default=0)
    nb_match_lose = models.IntegerField(default=0)
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE)
    main_char = models.ForeignKey('Character', on_delete=models.CASCADE,blank=True, null=True, related_name='main_char')
    second_char = models.ForeignKey('Character', on_delete=models.CASCADE,blank=True, null=True, related_name='second_char')
    third_char = models.ForeignKey('Character', on_delete=models.CASCADE,blank=True, null=True, related_name='third_char')
    saison = models.ForeignKey(Saison, on_delete=models.CASCADE)
    def __str__(self):
        return f"({self.saison.prefix} {self.saison.title} {self.saison.number})   {self.competitor} : {self.elo}"

class Tournament(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    event = models.CharField(max_length=255)
    event_slug = models.CharField(max_length=255, null=True)
    state = models.ForeignKey('Tournament_state', on_delete=models.CASCADE)
    saison = models.ManyToManyField(Saison, related_name='Saison')
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    association = models.ForeignKey('Association', on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.name

class Tournament_state(models.Model):
    state = models.CharField(max_length=255)
    def __str__(self):
        return self.state

class City(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Association(models.Model):
    name = models.CharField(max_length=255)
    logo_url = models.URLField(default="", null=True)
    site_url = models.URLField(default="", null=True)
    def __str__(self):
        return self.name

class Matchs(models.Model):
    fullRoundText = models.CharField(max_length=255)
    roundText = models.CharField(max_length=255)
    winner = models.ForeignKey('Competitor', on_delete=models.CASCADE, related_name='winner')
    looser = models.ForeignKey('Competitor', on_delete=models.CASCADE, related_name='looser')
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
    score = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.tournament.name} {self.roundText}   {self.winner} vs {self.looser} {self.score}"

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # La liaison OneToOne vers le modèle User
    competitor = models.OneToOneField(Competitor, on_delete=models.CASCADE, null=True, related_name='nom_smash')

    def __str__(self):
        return "Profil de {0}".format(self.user.username)

class Character(models.Model):
    name_fr = models.CharField(max_length=255, unique=True)
    name_en = models.CharField(max_length=255)
    icon_static = models.CharField(max_length=255)
    splash_url = models.URLField(default="", null=True)
    def __str__(self):
        return f"{self.name_fr}"

class Vod(models.Model):
    video_url = models.URLField(default="", null=True)
    id_watch_video = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
    # player_one = models.ForeignKey('Elo', on_delete=models.SET_NULL, null=True, related_name="player_one")
    # player_two = models.ForeignKey('Elo', on_delete=models.SET_NULL, null=True, related_name="player_two")
    def __str__(self):
        return f"{self.title}"