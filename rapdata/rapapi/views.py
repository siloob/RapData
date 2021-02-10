from django.shortcuts import render
from rest_framework import viewsets

from data.models import Artist
from .serializers import ArtistSerializer

# Create your views here.

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer