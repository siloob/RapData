from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework.settings import api_settings

from rest_framework.throttling import BaseThrottle, UserRateThrottle

class CustomThrottle(UserRateThrottle):
    
    def allow_request(self, request, view):
        group = request.user.groups.first()
        if group:
            self.scope = group.name
        else:
            return False

        self.rate = self.get_rate()
        self.num_requests, self.duration = self.parse_rate(self.rate)
        
        return super().allow_request(request, view)

class AdminRateThrottle(BaseThrottle):
    def allow_request(self, request, view):
        return True

