from django.urls import path
from . import views

urlpatterns = [
    path('analytics', views.all_events, name="events"),
    path('analytics_select_related', views.events_select_related, name="events_select_related"),
    path('analytics_offset', views.events_offset_paginated,
         name="events_offset"),
    path('analytics_keyset_pg', views.events_keyset_paginated_postgres,
         name="events_keyset_pg"),
    path('analytics_keyset_generic', views.events_keyset_paginated_generic,
         name="events_keyset_generic"),
    path('analytics/api', views.EventListView.as_view(),
         name="events_api")
]
