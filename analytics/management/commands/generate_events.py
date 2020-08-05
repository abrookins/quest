from django.core.management.base import BaseCommand

from analytics.models import Event


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

    def handle(self, *args, **options):
        events = []
        data = {
            "name": options['name'],
            "data": {"important!": "you rock"}
        }
        if options['user_id'] > 0:
            data['user_id'] = options['user_id']

        for i in range(options['num']):
            events.append(Event(**data))

        Event.objects.bulk_create(events)
