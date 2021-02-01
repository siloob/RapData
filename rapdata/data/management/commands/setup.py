from django.core.management.base import BaseCommand, CommandError

from data.models import MusicStoryTokens
from data.scripts.musicstory import get_tokens

CONSUMER_KEY = "601c462cff75f9784c8e7a1a417d61fd907afaec"
CONSUMER_SECRET = "be241d18513af9139e33202fd29fb5a92909884a"

class Command(BaseCommand):
    help = 'Setup for MusicStory,'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Deleting tokens'))
        MusicStoryTokens.objects.all().delete()

        token, token_secret = get_tokens(CONSUMER_KEY, CONSUMER_SECRET)

        MusicStoryTokens.objects.create(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            token=token,
            token_secret=token_secret)

        self.stdout.write(self.style.SUCCESS('Successfully add new tokens'))

        

        