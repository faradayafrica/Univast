# Django Imports
from django.http import HttpRequest

# Rest Framework Imports
from rest_framework.throttling import SimpleRateThrottle


class APIKeyThrottling(SimpleRateThrottle):
    scope = "rate"

    def get_cache_key(self, request: HttpRequest, view):
        authorization = request.headers.get("Authorization", None)
        if not authorization:
            return

        api_key = authorization.split(" ")[-1]
        return api_key
