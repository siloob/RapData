from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.authtoken.models import Token

from data.models import Artist
from rapapi.serializers import ArtistSerializer

# Create your views here.

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

class UserCreateView(APIView):
    permission_classes=[IsAdminUser]

    def post(self, request, format=None):
        data = request.data
        username = data['username']
        password = data['password']
        
        user, created = User.objects.get_or_create(username=username)
        if not created:
            return Response({"error": "username is not available"})
        
        user.password = password
        user.save()
        
        token = Token.objects.create(user=user)
        return Response({"token": token.key})