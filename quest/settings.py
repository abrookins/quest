"""
Django settings for quest project.

Compose sets QUEST_DATABASE_HOST=db and QUEST_REDIS_URL for the
container. On the host, defaults point at 127.0.0.1.
"""

import os
import warnings

# django-bulma 0.8.x still imports pkg_resources on startup.
warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API",
    category=UserWarning,
)

DATABASE_HOST = os.environ.get("QUEST_DATABASE_HOST", "127.0.0.1")
REDIS_URL = os.environ.get("QUEST_REDIS_URL", "redis://127.0.0.1:6379/0")
DATABASE_PASSWORD = os.environ.get("QUEST_DATABASE_PASSWORD", "test")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'u06zoy2&g+le1tr21om=j(545ct$j$fmo01(tpl@iki8h!y2_f'

DEBUG = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']

INSTALLED_APPS = [
    'quest',
    'goals.apps.GoalsConfig',
    'accounts.apps.AccountsConfig',
    'frontend.apps.FrontendConfig',
    'analytics.apps.AnalyticsConfig',
    'bulma',  # Comes first to override Django admin auth templates.
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',
    'debug_toolbar',
    #'silk',
]

MIDDLEWARE = [
    # 'django.middleware.cache.UpdateCacheMiddleware',  # Must be first
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',  # Must be last
]

ROOT_URLCONF = 'quest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'quest.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quest',
        'USER': 'quest',
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': os.environ.get("QUEST_DATABASE_PORT", "5432"),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = '/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'accounts.authentication.RedisTokenAuthentication',
    ]
}

CSRF_COOKIE_NAME = "csrftoken"

INTERNAL_IPS = ('127.0.0.1', '192.168.78.132', '192.168.78.1', '172.18.0.1')

EVENTS_PER_PAGE = 10

