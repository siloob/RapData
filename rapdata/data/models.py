from django.db import models

# Create your models here.

class Artist(models.Model):
    name = models.CharField(max_length=100)
    id_music_story = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta: 
        verbose_name = 'Artist'

class MusicStoryTokens(models.Model):
    consumer_key = models.CharField(max_length=50)
    consumer_secret = models.CharField(max_length=50)
    token = models.CharField(max_length=200)
    token_secret = models.CharField(max_length=200)

    class Meta: 
        verbose_name = 'Music Story'