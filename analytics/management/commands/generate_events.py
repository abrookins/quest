from django.core.management.base import BaseCommand

from analytics.models import Event

# Coordinates from the book's JSON indexing example (Corvallis, Oregon).
DEMO_LATITUDE = 44.523064
DEMO_LONGITUDE = -123.258


class Command(BaseCommand):
    help = 'Generate semi-random analytics events'

    def add_arguments(self, parser):
        parser.add_argument(
            '--num',
            type=int,
            default=1000)
        parser.add_argument(
            '--name',
            type=str,
            default='goal_viewed.generated')
        parser.add_argument(
            '--user-id',
            type=int,
            default=0)
        parser.add_argument(
            '--with-location',
            action='store_true',
            help=(
                'Set data.latitude/longitude so process_events can fetch '
                'cloud cover. Off by default: a large run plus process_events '
                'would hammer the free weather API.'
            ))

    def handle(self, *args, **options):
        events = []
        payload = {"important!": "you rock"}
        if options['with_location']:
            payload['latitude'] = DEMO_LATITUDE
            payload['longitude'] = DEMO_LONGITUDE
        data = {
            "name": options['name'],
            "data": payload
        }
        if options['user_id'] > 0:
            data['user_id'] = options['user_id']

        for i in range(options['num']):
            events.append(Event(**data))

        Event.objects.bulk_create(events)
        self.stdout.write(f"Created {options['num']} events.")
