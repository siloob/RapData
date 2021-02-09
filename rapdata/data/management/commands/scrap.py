from django.core.management.base import BaseCommand, CommandError
import logging

from data.models import RapGeniusTokens, Artist
from data.scripts.scrap import get_twitter_datas, get_instagram_datas, get_facebook_datas

dblogger = logging.getLogger("dblogger")

class Command(BaseCommand):
    help = 'scrap daats, -t twitter, _f facebook, -i instagram'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '-i',
            '--instagram',
            help='get instagram datas',
            action='store_true'
        )

        parser.add_argument(
            '-t',
            '--twitter',
            help='get twitter datas',
            action='store_true'
        )

        parser.add_argument(
            '-f',
            '--facebook',
            help='get facebook datas',
            action='store_true'
        )

    def scrap_twitter(self):
        artists = Artist.objects.filter(twitter_name__isnull=False)
        for artist in artists:
            nb_followers = get_twitter_datas(artist.twitter_name)
            #print(nb_followers)
            break

    def scrap_instagram(self):
        artists = Artist.objects.exclude(instagram_name__exact='').exclude(instagram_name__isnull=True)
        
        for artist in artists:
            nb_followers = get_instagram_datas(artist.instagram_name)
            artist.instagram_followers = nb_followers
            artist.save()
            dblogger.info(('[UPDATE] artist %s added instagram followers : %i' % (artist.name, artist.instagram_followers)))

    def scrap_facebook(self):
        artists = Artist.objects.exclude(facebook_name__exact='').exclude(facebook_name__isnull=True)
        cpt = 0
        for artist in artists:
            nb_followers = get_facebook_datas(artist.facebook_name)
            if nb_followers:
                artist.facebook_followers = nb_followers
                artist.save()
                dblogger.info(('[UPDATE] artist %s added facebook followers : %i' % (artist.name, artist.facebook_followers)))
                cpt += 1
        
        self.stdout.write(self.style.SUCCESS('Successfully update facebook followers for %i artists' % cpt))


    def handle(self, *args, **options):
        if options['twitter']:
            self.scrap_twitter()
        elif options['instagram']:
            self.scrap_instagram()
        elif options['facebook']:
            self.scrap_facebook()
        else:
            print('grosse merde')