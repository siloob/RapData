from django.contrib import admin

from data.models import Artist, MusicStoryTokens, RapGeniusTokens

# Register your models here.

admin.site.register(Artist)
admin.site.register(MusicStoryTokens)
admin.site.register(RapGeniusTokens)