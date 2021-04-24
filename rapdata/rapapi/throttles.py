from django.core.cache import caches
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework.settings import api_settings

from rest_framework.throttling import BaseThrottle, UserRateThrottle

class CustomThrottle(UserRateThrottle):
    def allow_request(self, request, view):
        if request.user.is_staff:
            return True

        if self.rate is None:
            return True

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        group = request.user.groups.first()
        if group:
            self.scope = group.name
        else:
            return self.throttle_failure()

        self.rate = self.get_rate()
        self.num_requests, self.duration = self.parse_rate(self.rate)

        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        if len(self.history) >= self.num_requests:
            return self.throttle_failure()

        return self.throttle_success()

