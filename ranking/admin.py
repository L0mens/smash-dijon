from django.contrib import admin
from django.forms import TextInput
from django.db import models

from .models import (Association, Character, City, Competitor, Elo, Matchs, MessageInfo,
                     Profil, Saison, Tournament, Tournament_place,
                     Tournament_serie, Tournament_state, Vod, Vodplaylist)

class MessageModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'255'})},
        }


# Register your models here.
admin.site.register(Competitor)
admin.site.register(Tournament)
admin.site.register(Matchs)
admin.site.register(Saison)
admin.site.register(Elo)
admin.site.register(City)
admin.site.register(Profil)
admin.site.register(Association)
admin.site.register(Character)
admin.site.register(MessageInfo, MessageModelAdmin)
admin.site.register(Vod)
admin.site.register(Vodplaylist)
admin.site.register(Tournament_state)
admin.site.register(Tournament_serie)
admin.site.register(Tournament_place)
