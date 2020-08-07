import logging

from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import exceptions

from quest.connections import redis_connection
from quest import redis_key_schema


User = get_user_model()
redis = redis_connection()
log = logging.getLogger(__name__)


class RedisTokenAuthentication(authentication.BaseAuthentication):
    def _get_token(self, request):
        header = request.META.get('HTTP_AUTHORIZATION')
        if not header:
            return None

        parts = header.split()

        if parts[0] != 'Token':
            return None
        if len(parts) != 2:
            log.info(f"Token auth failed: invalid auth header {header}")
            raise exceptions.AuthenticationFailed('Invalid token')

        return parts[1]

    def authenticate(self, request):
        token = self._get_token(request)
        key = redis_key_schema.auth_token(token)
        user_id = redis.get(key)

        if not user_id:
            log.info(f"Token auth failed: token {token} not found in redis")
            raise exceptions.AuthenticationFailed(f'Invalid token')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            log.info(f"Token auth failed: user {user_id} does not exist")
            raise exceptions.AuthenticationFailed('Invalid token')

        return user, None
