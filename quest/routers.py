import random

import mmh3

from quest.middleware.router_middleware import request_config


class PrimaryReplicaRouter:
    """
    Example primary/replica router adapted from:
    https://docs.djangoproject.com/en/3.1/topics/db/multi-db/
    """
    def db_for_read(self, model, **hints):
        """
        Reads go to the replica.
        """
        return 'replica'

    def db_for_write(self, model, **hints):
        """
        Writes always go to primary.
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the primary/replica pool.
        """
        db_set = {'default', 'replica'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True


# NOTE: This example application only includes one replica.
# To use this router, configure two replicas and name them
# "replica1" and "replica2" in the DATABASES setting.
REPLICAS = ['replica1', 'replica2']


def hash_to_bucket(user_id, num_buckets):
    """Consistently hash `user_id` into buckets of length `num_buckets`.

    Approach derived from: https://stats.stackexchange.com/questions/26344/how-to-uniformly-project-a-hash-to-a-fixed-number-of-buckets
    """
    i = mmh3.hash128(str(user_id))
    p = i / float(2**128)
    for j in range(0, num_buckets):
        if j / float(num_buckets) <= p and (j + 1) / float(num_buckets) > p:
            return j + 1
    return num_buckets


class HashingPrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        """Consistently direct reads of authenticated users to the same replica.

        Uses MurmurHash3 for the hashing function.
        """
        user_id = getattr(request_config, 'user_id', None)
        if user_id:
            bucket = hash_to_bucket(user_id)
            return REPLICAS[bucket]
        return random.choice(REPLICAS)
