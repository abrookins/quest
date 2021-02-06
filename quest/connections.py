import logging

from django.conf import settings
import redis


log = logging.getLogger(__name__)


def redis_connection(url=settings.REDIS_URL, decode_responses=True):
    return redis.Redis.from_url(url, decode_responses=decode_responses)
