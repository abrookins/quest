from quest.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quest',
        'USER': 'quest',
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': PRIMARY_HOST
    }
}

DATABASE_ROUTERS = []
