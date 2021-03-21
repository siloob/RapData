from django.contrib import admin

from data.models import Artist, MusicStoryTokens, RapGeniusTokens

# Register your models here.

class ArtistAdmin(admin.ModelAdmin):
    search_fields = ('name',)

admin.site.register(Artist, ArtistAdmin)
admin.site.register(MusicStoryTokens)
admin.site.register(RapGeniusTokens)