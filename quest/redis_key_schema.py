from django.conf import settings


DEFAULT_KEY_PREFIX = "quest-test"
PREFIX = getattr(settings, 'REDIS_KEY_PREFIX', DEFAULT_KEY_PREFIX)


def prefixed_key(f):
    """
    A method decorator that prefixes return values.

    Prefixes any string that the decorated method `f` returns with the value of
    the `REDIS_KEY_PREFIX` Django setting.
    """
    def prefixed_method(self, *args, **kwargs):
        key = f(self, *args, **kwargs)
        return f"{PREFIX}:{key}"

    return prefixed_method


@prefixed_key
def auth_token(token):
    """
    A token stored for a user.

    Format: token:[token]
    """
    return f"token:{token}"


@prefixed_key
def admin_goals_dashboard():
    """
    The rendered Admin Goals Dashboard.

    Format: admin:goals-dashboard
    """
    return "admin:goals-dashboard"


@prefixed_key
def task(uuid):
    """
    Task data.

    Format: task:[uuid]
    """
    return f"task:{uuid}"
