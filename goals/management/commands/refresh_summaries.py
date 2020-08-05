from django.core.management.base import BaseCommand
from django.db import connection, transaction

from goals.models import GoalSummary


class Command(BaseCommand):
    help = 'Refresh Goal summaries'

    def handle(self, *args, **options):
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY goals_summaries")
