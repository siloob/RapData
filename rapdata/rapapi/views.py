import logging
from http import HTTPStatus
from rapapi.scripts.mail_helper import send_email

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.authtoken.models import Token

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
        username = data['pseudo']
        
        user, created = User.objects.get_or_create(username=username)
        if not created:
            return Response({"error": "username is not available"}, status=HTTPStatus.IM_A_TEAPOT)
        
        user.password = data['password']
        user.first_name = data['pseudo']
        user.email = data['email']
        user.save()
        apilogger.info('[CREATE] user %s created' % user.username)

        user_group = Group.objects.get(name='user') 
        user_group.user_set.add(user)
        
        token = Token.objects.create(user=user)

        send_email(
            'Your token for rapdata',
            'Hello %s tanks for subscribing.\nHere is your token : %s' % (data['pseudo'], token.key),
            'rapdatafr@gmail.com',
            data['email']
        )

        return Response({"token": token.key})

def comment_is_correct(user_email,user_pseudo, user_comment):
    return True

class sendMail(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        data = request.data
        result = 0
        user_email = data['email']
        user_pseudo = data['pseudo']
        user_comment = data['comment']
        if comment_is_correct(user_email,user_pseudo, user_comment):
            result = send_email(
                'New comment by %s' % user_pseudo,
                user_comment,
                user_email,
                'rapdatafr@gmail.com'
            )
        return Response(result)

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

