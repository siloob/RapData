from django.core.management.base import BaseCommand, CommandError
import logging

from data.models import MusicStoryTokens, RapGeniusTokens
from data.scripts.musicstory import init_tokens

MS_CONSUMER_KEY = "601c462cff75f9784c8e7a1a417d61fd907afaec"
MS_CONSUMER_SECRET = "be241d18513af9139e33202fd29fb5a92909884a"

RG_CLIENT_ID = 'cibs5j1_xTZO8gPA-rGiZDzkj2T1Gtl9EAgRgzfzSdq7BQey23amLPSyAjImiGLH'
RG_CLIENT_SECRET = 'vTMtcvGxvVS7kuZ00v1K91mx5PycbpUP1NOJtJ3WMyAU7-xYvJWwoMl5eakVEC7bWXc-EX8-rUfy1Fiz5p4pfw'
RG_CLIENT_ACCESS_TOKEN = 'T-LMKo5UwXrMJEMrWG1XzbdWSSo5zcKFrI2CwUQaGHpKUr_xIf1ppHvMaNubrycy'

dblogger = logging.getLogger("dblogger")

class Command(BaseCommand):
    help = 'Init musicstory, rap genius tokens'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Deleting tokens'))

        MusicStoryTokens.objects.all().delete()
        dblogger.info('[DELETE] MUSICSTORY TOKENS')
        
        RapGeniusTokens.objects.all().delete()
        dblogger.info('[DELETE] RAPGENIUS TOKENS')

        consumer_key, consumer_secret, token, token_secret = init_tokens(MS_CONSUMER_KEY, MS_CONSUMER_SECRET)

        MusicStoryTokens.objects.create(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            token=token,
            token_secret=token_secret
        )

        dblogger.info('[INSERT] MUSICSTORY TOKENS')

        RapGeniusTokens.objects.create(
            client_id=RG_CLIENT_ID,
            client_secret=RG_CLIENT_SECRET,
            client_access_token=RG_CLIENT_ACCESS_TOKEN
        )
        
        dblogger.info('[INSERT] RAPGENIUS TOKENS')

        self.stdout.write(self.style.SUCCESS('Successfully add new tokens'))