import contextlib
import gc
import os
import sys
import time

project_path = os.path.split(
    os.path.abspath(os.path.dirname(__file__)))[0]
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "quest.settings")
sys.path.append(project_path)

# Load models
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import psutil

# Disable garbage collection to get a more accurate
# idea of how much memory is used.
gc.disable()

from analytics.models import Event


def mb_used():
    """Return the number of megabytes used by the current process."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1e+6


@contextlib.contextmanager
def profile():
    """A context manager that measures MB and CPU time used."""
    snapshot_before = mb_used()
    time_before = time.time()

    yield

    time_after = time.time()
    snapshot_after = mb_used()

    print("{} mb used".format(snapshot_after - snapshot_before))
    print("{} seconds elapsed".format(time_after - time_before))
    print()


def main():
    if not len(sys.argv) == 2 or \
            sys.argv[1] not in ('values', 'models'):
        print("Usage: python values.py <models|values>")
        exit(1)

    if sys.argv[1] == 'values':
        print("Running values query -- 1,000,000 records")
        with profile():
            events = Event.objects.all()[:1000000].values(
                'name', 'data')
            for e in events:
                e['name']
                e['data']
    elif sys.argv[1] == 'models':
        print("Running ORM query -- 1,000,000 records")
        with profile():
            for e in Event.objects.all()[:1000000]:
                e.name
                e.data


if __name__ == '__main__':
    main()
