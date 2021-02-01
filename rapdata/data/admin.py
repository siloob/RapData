from django.contrib import admin

from data.models import Artist, MusicStoryTokens

# Register your models here.

admin.site.register(Artist)
admin.site.register(MusicStoryTokens)