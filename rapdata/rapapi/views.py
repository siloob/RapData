import logging

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import Throttled

from data.models import Artist
from rapapi.serializers import ArtistSerializer
from rapapi.throttles import CustomThrottle

# Create your views here.

apilogger = logging.getLogger('apilogger')

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all().order_by('id')
    serializer_class = ArtistSerializer
    throttle_classes = [CustomThrottle]

    class Meta:
        ordering = ['-id']

class UserCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        data = request.data
        username = data['username']
        password = data['password']
        
        user, created = User.objects.get_or_create(username=username)
        if not created:
            return Response({"error": "username is not available"})
        
        user.password = password
        user.save()
        apilogger.info('[CREATE] user %s created' % user.username)

        user_group = Group.objects.get(name='user') 
        user_group.user_set.add(user)

        
        token = Token.objects.create(user=user)
        return Response({"token": token.key})


class GetRequestLimit(APIView):
    throttle_classes = [CustomThrottle]  

    def max_data(self,datas):
        result = ({"nb_requests_max":0,"nb_requests":0})
        for data in datas:
            if data[0] > result["nb_requests_max"]:
                result["nb_requests_max"] = data[0]
                result["nb_requests"] = data[1]
        return result

    def get_nb_requests(self, request):
        throttle_datas = []
        for throttle in self.get_throttles():
            if throttle.allow_request(request, self):
                nb_requests_max = throttle.parse_rate(throttle.get_rate())[0]
                nb_requests = len(throttle.cache.get(throttle.key, []))
                throttle_datas.append((nb_requests_max, nb_requests))
        
        return self.max_data(throttle_datas) 

    def get(self, request, format=None):
        return Response(self.get_nb_requests(request))

