import datetime

from darksky.api import DarkSky
from django.core.management.base import BaseCommand
from django.conf import settings

from analytics.models import Event


darksky = DarkSky(settings.DARK_SKY_API_KEY)


class Command(BaseCommand):
    help = 'Annotate events with cloud cover data'

    def add_arguments(self, parser):
        today = datetime.date.today()
        default_start = today - datetime.timedelta(days=30)
        default_end = today

        parser.add_argument(
            '--start',
            type=lambda s: datetime.datetime.strptime(
                s,
                '%Y-%m-%d-%z'
            ),
            default=default_start)
        parser.add_argument(
            '--end',
            type=lambda s: datetime.datetime.strptime(
                s,
                '%Y-%m-%d-%z'
            ),
            default=default_end)

    def handle(self, *args, **options):
        events = Event.objects.filter(
            created_at__range=[options['start'],
                               options['end']])
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
                forecast = darksky.get_time_machine_forecast(
                    latitude, longitude, e.created_at)
                hourly = forecast.hourly.data[e.created_at.hour]
                e.data['weather']['cloud_cover'] = \
                    hourly.cloud_cover

            # This could alternatively be done with bulk_update().
            # Doing so would in theory consume more memory but take
            # less time.
            e.save()
