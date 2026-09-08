import datetime

import requests
from django.core.management.base import BaseCommand

from analytics.models import Event

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"


def cloud_cover_at(latitude, longitude, when):
    """Return hourly cloud cover (0-100) from Open-Meteo's free archive API."""
    when_utc = when.astimezone(datetime.timezone.utc)
    day = when_utc.date().isoformat()
    response = requests.get(
        ARCHIVE_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "start_date": day,
            "end_date": day,
            "hourly": "cloud_cover",
            "timezone": "UTC",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["hourly"]["cloud_cover"][when_utc.hour]


class Command(BaseCommand):
    help = 'Annotate events with cloud cover data'

    def add_arguments(self, parser):
        today = datetime.datetime.now(datetime.timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0)
        parser.add_argument(
            '--start',
            type=lambda s: datetime.datetime.strptime(
                s,
                '%Y-%m-%d-%z'
            ),
            default=today - datetime.timedelta(days=30))
        parser.add_argument(
            '--end',
            type=lambda s: datetime.datetime.strptime(
                s,
                '%Y-%m-%d-%z'
            ),
            default=today + datetime.timedelta(days=1))

    def handle(self, *args, **options):
        events = Event.objects.filter(
            created_at__range=[options['start'],
                               options['end']])
        annotated = 0
        for e in events.exclude(
                data__latitude=None,
                data__longitude=None).iterator():  # <1>

            # Presumably we captured a meaningful latitude and
            # longitude related to the event (perhaps the
            # user's location).
            latitude = float(e.data.get('latitude'))
            longitude = float(e.data.get('longitude'))

            if 'weather' not in e.data:
                e.data['weather'] = {}

            if 'cloud_cover' not in e.data['weather']:
                e.data['weather']['cloud_cover'] = cloud_cover_at(
                    latitude, longitude, e.created_at)

            # This could alternatively be done with bulk_update().
            # Doing so would in theory consume more memory but take
            # less time.
            e.save()
            annotated += 1

        if annotated:
            self.stdout.write(f"Annotated {annotated} events.")
        else:
            self.stdout.write("No events had latitude/longitude.")
