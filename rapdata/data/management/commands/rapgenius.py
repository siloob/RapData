from django.core.management.base import BaseCommand, CommandError
import logging

from data.models import RapGeniusTokens, Artist
from data.scripts.rapgenius import get_id, get_data

dblogger = logging.getLogger("dblogger")

class Command(BaseCommand):
    help = 'get genius info, -i for ids, -d for datas'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '-i',
            '--id',
            help='get genius ids',
            action='store_true'
        )

        parser.add_argument(
            '-d',
            '--data',
            help='get genius data',
            action='store_true'
        )

        parser.add_argument(
            '-a',
            '--all',
            help='girst get genius ids then get genius data',
            action='store_true'
        )

    def get_ids(self):
        tokens = RapGeniusTokens.objects.all().first()
        artists = Artist.objects.filter(id_rap_genius__isnull=True)        
        cpt = 0

        for artist in artists:
            id_rap_genius = get_id(tokens.client_access_token, artist.name)
            if id_rap_genius:
                artist.id_rap_genius = id_rap_genius
                artist.save()
                dblogger.info('[UPDATE] added %s id_rap_genius %i' % (artist.name, artist.id_rap_genius))
                cpt += 1

        self.stdout.write(self.style.SUCCESS('Successfully added %i id_rap_genius' % cpt))

    def get_datas(self):
        tokens = RapGeniusTokens.objects.all().first()
        artists = Artist.objects.filter(id_rap_genius__isnull=False)

        nb_save = 0
        for artist in artists:
            datas = get_data(tokens.client_access_token, artist.id_rap_genius)
            artist.update_genius_data(datas)
            artist.save()
            dblogger.info('[UPDATE] added genius datas to %s' % artist.name)    
            nb_save += 1

        self.stdout.write(self.style.SUCCESS('Successfully added genius datas for %i artists' % nb_save))

    def handle(self, *args, **options):
        if options['id']:
            self.get_ids()
        elif options['data']:
            self.get_datas()
        elif options['all']:
            self.get_ids()
            self.get_datas()
        else:
            print('grosse merde')