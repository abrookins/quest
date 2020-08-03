from django.conf import settings
from django.urls import include, path

from .admin import admin_site

urlpatterns = [
    path('', include('frontend.urls')),
    path('', include('goals.urls')),
    path('', include('accounts.urls')),
    path('', include('analytics.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin_site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
