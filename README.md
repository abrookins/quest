# Quest

Example Django project for [The Temple of Django Database Performance](https://spellbookpress.com/books/temple-of-django-database-performance/) by Andrew Brookins.

This tree is the `code/` submodule of the book repo, on branch `temple-book`. Listings in the book `include::` files from here.

## Versions

The runnable app targets **Python 3.12** and **Django 4.2**. That is the last LTS whose ORM APIs still match the book (`select_related`, `prefetch_related`, `iterator`, `JSONField`, GIN indexes, concurrent index operations) without rewriting the listings.

Django 3.0 (the original pin) does not install on Apple Silicon and does not run against Postgres 15+.

## Setup (Docker)

Docker is the default. Postgres, Redis, and Django run as Compose services. This is also the path later updates will use when the profiling chapter grows a local Grafana and OpenTelemetry stack.

From this directory:

    make build
    make dev          # http://127.0.0.1:8000/
    make test
    make superuser

If port 8000 is already taken:

    QUEST_WEB_PORT=8001 make dev

Postgres is published on host port 15432 (`psql -h 127.0.0.1 -p 15432 -U quest`). Redis stays on the Compose network so it does not collide with a host `redis-server`.

    make logs         # follow Django
    make down         # stop the stack
    make generate-events NUM=500000 USER_ID=1

Frontend asset watch is opt-in: `docker compose --profile frontend up`.

## Without Docker

Postgres 16 and Redis on the host, plus a Python 3.12 venv. On macOS:

    brew install postgresql@16 redis
    brew services start postgresql@16
    brew services start redis

If `brew services` does not listen:

    pg_ctl -D /opt/homebrew/var/postgresql@16 start
    redis-server --daemonize yes

Then:

    make local-setup    # .venv, role/database `quest` / password `test`, migrate
    make local-test
    make local-run      # http://127.0.0.1:8000/  (PORT=8001 if needed)
    make local-superuser

## The N+1 demo

`GET /analytics` is intentionally N+1 (`Event.objects.all()`, template walks `event.user.profile.account`). `GET /analytics_select_related` is the book's fix. Do not add `select_related` to `all_events` or the chapter demo disappears.

## Weather annotation

`process_events` writes hourly cloud cover from [Open-Meteo](https://open-meteo.com/en/docs/historical-weather-api). No API key.

`generate_events` does not add coordinates (a 500k run plus weather would blow the free 10,000 calls/day cap). For a small weather demo, with the Compose stack up:

    docker compose exec web python manage.py generate_events --num 5 --user-id 1 --with-location
    docker compose exec web python manage.py process_events

## Generating data for performance problems

    make generate-events NUM=500000 USER_ID=1

`USER_ID` is a Django user id (your superuser is usually `1`). The web container must already be running (`make dev`).

## Copyright

This example code is copyright 2020–2026 Andrew Brookins.
