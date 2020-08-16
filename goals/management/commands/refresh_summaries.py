from django.core.management.base import BaseCommand
from django.db import connection, transaction


# tag::refreshing-materialized-views[]
class Command(BaseCommand):
    help = 'Refresh Goal summaries'

    def handle(self, *args, **options):
        with transaction.atomic():
            with connection.cursor() as cursor:  # <1>
                cursor.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY goals_summaries")  # <2>
# end::refreshing-materialized-views[]
