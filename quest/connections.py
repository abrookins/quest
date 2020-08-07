import logging

from django.conf import settings
import redis


log = logging.getLogger(__name__)


def redis_connection():
    return redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
