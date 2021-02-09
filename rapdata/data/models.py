from django.db import models

# Create your models here.

class Artist(models.Model):
    name = models.CharField(max_length=100)

    id_music_story = models.IntegerField()

    id_rap_genius = models.IntegerField(default=None,null=True, blank=True)
    genius_followers = models.IntegerField(default=None,null=True, blank=True)
    genius_image = models.URLField(default=None,null=True, blank=True)
    genius_url = models.URLField(default=None,null=True, blank=True)

    instagram_name = models.CharField(max_length=100,default=None,null=True, blank=True)
    instagram_followers = models.IntegerField(default=None,null=True, blank=True)

    facebook_name = models.CharField(max_length=100,default=None,null=True, blank=True)
    twitter_name = models.CharField(max_length=100,default=None,null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta: 
        verbose_name = 'Artist'

    def update_genius_data(self,datas):
        self.facebook_name = datas['facebook_name']
        self.twitter_name = datas['twitter_name']
        self.instagram_name = datas['instagram_name']
        self.genius_followers = datas['genius_followers']
        self.genius_image = datas['genius_image']
        self.genius_url = datas['genius_url']

class MusicStoryTokens(models.Model):
    consumer_key = models.CharField(max_length=50)
    consumer_secret = models.CharField(max_length=50)
    token = models.CharField(max_length=200)
    token_secret = models.CharField(max_length=200)

    class Meta: 
        verbose_name = 'MusicStory Token'

class RapGeniusTokens(models.Model):
    client_id = models.CharField(max_length=200)
    client_secret = models.CharField(max_length=200)
    client_access_token = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'RagGenius Token'