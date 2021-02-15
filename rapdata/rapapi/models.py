from django.db import models
from rest_framework import viewsets

from rapapi.serializers import ArtistSerializer
from data.models import Artist

# Create your models here.

class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    artists = Artist.objects.all().order_by('id')
    serializer_class = ArtistSerializer

    class Meta:
        ordering = ['-id']