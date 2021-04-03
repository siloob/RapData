from django.core.management.base import BaseCommand, CommandError
import logging

from data.models import RapGeniusTokens, Artist
from data.scripts.scrap import get_twitter_datas, get_instagram_datas, get_facebook_datas, get_insta_cookies
import data.scripts.seleniummanager as seleniummanager

dblogger = logging.getLogger("dblogger")

class Command(BaseCommand):
    help = 'scrap daats, -t twitter, -f facebook, -i instagram'
    
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
        count = 0
        artists = Artist.objects.filter(twitter_name__isnull=False)
        driver = seleniummanager.start_browser()
        for artist in artists:
            nb_followers = get_twitter_datas(driver, artist.twitter_name)
            if nb_followers is not None:
                artist.twitter_followers = nb_followers
                artist.save()
                count += 1
        seleniummanager.exit_browser(driver)
        dblogger.info('[UPDATE] %i twitter followers added' % count)

    def scrap_instagram(self):
        count = 0
        cookies = get_insta_cookies()
        if cookies is not None:
            driver = seleniummanager.start_browser()
            driver = seleniummanager.init_driver_insta(driver, cookies)
            artists = Artist.objects.exclude(instagram_name__exact='').exclude(instagram_name__isnull=True)

            for artist in artists:
                nb_followers = get_instagram_datas(driver, artist.instagram_name, cookies)
                artist.instagram_followers = nb_followers
                artist.save()
                count += 1

            dblogger.info(('[UPDATE] added instagram followers : %i' % count))
            seleniummanager.exit_browser(driver)

    def scrap_facebook(self):
        artists = Artist.objects.exclude(facebook_name__exact='').exclude(facebook_name__isnull=True)
        cpt = 0
        driver = seleniummanager.start_browser()
        driver = seleniummanager.connect_facebook(driver)
        for artist in artists:
            nb_followers = get_facebook_datas(driver, artist.facebook_name)
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