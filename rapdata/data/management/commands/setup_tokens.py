from django.core.management.base import BaseCommand, CommandError
import logging

from data.models import MusicStoryTokens
from data.scripts.musicstory import init_tokens

CONSUMER_KEY = "601c462cff75f9784c8e7a1a417d61fd907afaec"
CONSUMER_SECRET = "be241d18513af9139e33202fd29fb5a92909884a"

dblogger = logging.getLogger("dblogger")

class Command(BaseCommand):
    help = 'Init musicstory tokens'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Deleting tokens'))
        MusicStoryTokens.objects.all().delete()
        dblogger.info('[DELETE] MUSICSTORY TOKENS')

        consumer_key, consumer_secret, token, token_secret = init_tokens(CONSUMER_KEY, CONSUMER_SECRET)

        MusicStoryTokens.objects.create(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            token=token,
            token_secret=token_secret)

        dblogger.info('[INSERT] MUSICSTORY TOKENS')

        self.stdout.write(self.style.SUCCESS('Successfully add new tokens'))