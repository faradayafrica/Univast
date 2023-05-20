# Stdlib Imports
from typing import Dict, Tuple

# Django Imports
from django.http import HttpRequest
from django.core.exceptions import ImproperlyConfigured

# Rest Framework Imports
from rest_framework.exceptions import NotFound
from rest_framework.throttling import SimpleRateThrottle

# Own Imports
from academia.models import ClientAPIKey


class APIKeyThrottling(SimpleRateThrottle):
    rate: str
    scope: str
    THROTTLE_RATES: Dict[str, str] = {}

    @classmethod
    def get_client_scope_and_rate(cls, api_key: str) -> Tuple[str, int]:
        try:
            client_apikey: ClientAPIKey = ClientAPIKey.objects.get_from_key(
                key=api_key
            )
        except ClientAPIKey.DoesNotExist:
            raise NotFound({"message": "Api-Key does not exist!"})
        return client_apikey.scope, client_apikey.rate

    def get_cache_key(self, request: HttpRequest, view):
        authorization = request.headers.get("Authorization", None)
        if not authorization:
            return

        api_key = authorization.split(" ")[-1]
        client_scope, _ = self.get_client_scope_and_rate(api_key)

        self.scope = client_scope
        self.get_rate()

        return self.cache_format % {
            "scope": client_scope,
            "ident": api_key,
        }

    def get_rate(self):
        request = self.request
        if request is None:
            return None

        authorization = request.headers.get("Authorization", None)
        if not authorization:
            return

        api_key = authorization.split(" ")[-1]
        client_scope, client_rate = self.get_client_scope_and_rate(api_key)
        if not client_rate:
            msg = f"No default throttle rate set for {client_scope} scope"
            raise ImproperlyConfigured(msg)

        # Store the rate in the cache
        self.THROTTLE_RATES[self.scope] = f"{client_rate}/hour"
        return f"{client_rate}/hour"
