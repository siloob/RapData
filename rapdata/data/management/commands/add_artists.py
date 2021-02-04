from django.core.management.base import BaseCommand, CommandError

from data.models import MusicStoryTokens, Artist
from data.scripts.musicstory import get_artists

dblogger = logging.getLogger("dblogger")

class Command(BaseCommand):
    help = 'actualize artist list'

    def handle(self, *args, **options):
        tokens = MusicStoryTokens.objects.all().first()
        artists = get_artists(tokens.consumer_secret, tokens.token, tokens.token_secret)
        nb_obj_existing = 0
        
        for artist in artists:
            obj, created = Artist.objects.all().get_or_create(
                name=artist[0], 
                id_music_story=artist[1])
            
            if not created:
                nb_obj_existing += 1
            else:
                dblogger.info('[INSERT] MUSICSTORY ARTIST ADDED : %s | %s' % (obj.name, obj.id_music_story))

        self.stdout.write(self.style.SUCCESS('Successfully added %i new artist' % int(len(artists) - nb_obj_existing)))
        self.stdout.write(self.style.SUCCESS('%i artists still in base' % nb_obj_existing))
        

        

        