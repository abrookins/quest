# Agent instructions

**Quest** is the example Django project for *The Temple of Django Database Performance*. It is a teaching app, not a product. The book `include::`s tagged regions from this tree.

Canonical clone: `https://github.com/abrookins/quest` on branch **`temple-book`**. When this directory is the `code/` submodule of the book repo, commit here first, then update the submodule pointer in the parent.

## What to do here

- Change models, views, tests, and management commands that the book cites.
- Keep Docker / Compose / Make working so a reader can `make dev` and `make test`.
- Do not “modernize” the stack or clean up intentional slow paths unless the user is starting a new edition.

## Layout

| Path | Role |
|------|------|
| `quest/` | Project package: settings, URLs, custom admin, Redis helpers |
| `analytics/` | Events, N+1 / pagination / JSONB / weather demos |
| `goals/` | Goals/tasks, DRF API, materialized `GoalSummary` |
| `accounts/` | Profile/account, signup, Redis token auth |
| `frontend/` | Django pages plus React/webpack (opt-in) |
| `profile_values.py` | Included as a whole-file listing |
| `docker-compose.yml`, `Dockerfile`, `Makefile` | Default run path |
| `requirements.txt` | Pinned runtime + pytest |

## Non-negotiables

1. **Python 3.12 and Django 4.2.** Last LTS whose ORM surface matches the book. Do not bump to Django 5.x or rewrite listings to “current” APIs unless asked.
2. **Do not fix `all_events`.** `GET /analytics` (`Event.objects.all()`, template walks `event.user.profile.account`) is the N+1 demo. The fix is `events_select_related` at `GET /analytics_select_related`.
3. **Preserve Asciidoctor tags.** Regions `# tag::Name[]` / `# end::Name[]` are book listings. Renaming, deleting, or moving them without updating the book breaks the PDF/EPUB build. Same for `# <1>` callouts inside tagged code.
4. **Keep tagged blocks book-narrow.** Break lines earlier than PEP 8. Do not add type hints, extra comments, or reformatting inside a tagged region unless the listing in the book should change too.
5. **`setuptools==80.10.2` stays.** django-bulma 0.8.x still imports `pkg_resources`; setuptools 81+ warns and 82+ drops it.
6. **Do not enable Silk in `INSTALLED_APPS` by default.** It is mentioned in the book; the import is commented on purpose.
7. **Do not publish Redis to the host** in Compose. Postgres is on **15432** so it does not fight a local cluster; Redis stays on the Compose network.

This is a local demo: `DEBUG = True` and a hardcoded `SECRET_KEY` are expected. Do not turn it into a production-hardening exercise.

## Apps and demos

- **N+1:** `analytics/views.py` `all_events` vs `events_select_related`; template `analytics/templates/analytics/events.html`.
- **Offset pagination:** `events_offset_paginated` (`/analytics_offset`), `EVENTS_PER_PAGE`.
- **Keyset pagination:** Postgres-specific and generic views (`/analytics_keyset_pg`, `/analytics_keyset_generic`).
- **F() / `Func` / JSONB:** tagged helpers on the Event views; tests in `analytics/tests/`.
- **Partial index:** `Event.Meta.indexes` excludes `name="goal_viewed"`.
- **Materialized view:** `GoalSummary` is `managed = False`; refresh via `goals/management/commands/refresh_summaries.py`.
- **Weather:** `process_events` calls Open-Meteo (no API key). `generate_events` does **not** add coordinates unless `--with-location`. A 500k generate plus weather would blow the free 10k calls/day cap.

## Tagged listings (keep names stable)

`UserProfile`, `Account`, `Event`, `unpaginated`, `paginated`, `keyset_pagination_pg`, `keyset_pagination_generic`, `increment_all_event_versions`, `increment_all_event_versions_f_expression`, `update_all_events`, `update_all_events_func`, `Task`, `TaskStatus`, `Goal`, `GoalSummary`, `goal-view-a`, `goal-serializer-a/b/c`, `counting-with-python`, `counting-with-sql`, `aggregations`, `querying-materialized-views`, `refreshing-materialized-views`, plus test tags `fixtures`, `test_only`, `test_only_with_relations`, `test_defer`, `testing_jsonb_incrementer`.

If you add a listing the book will include, wrap it in a new `tag::` / `end::` pair.

## Run and test

Docker is the default (Postgres 16, Redis 7, Django). From this directory:

```
make build
make dev          # http://127.0.0.1:8000/
make test         # pytest in Compose
make superuser
make generate-events NUM=500000 USER_ID=1
```

Port 8000 busy: `QUEST_WEB_PORT=8001 make dev`. Compose env: `QUEST_DATABASE_HOST=db`, `QUEST_DATABASE_PASSWORD=test`, `QUEST_REDIS_URL=redis://redis:6379/0`.

Host venv (Postgres 16 + Redis on the machine, `uv`): `make local-setup`, `make local-test`, `make local-run`. Defaults: user/db `quest`, password `test`, host `127.0.0.1:5432`.

Frontend watch is opt-in: `docker compose --profile frontend up` (Node 22, webpack 4, React 16). Do not upgrade the JS toolchain unless the user asks; it is not the book’s focus.

`make test` should stay green. Tests use pytest-django (`pytest.ini` sets `DJANGO_SETTINGS_MODULE = quest.settings`).

## Data commands

```
make generate-events NUM=500000 USER_ID=1   # web container must already be up
docker compose exec web python manage.py generate_events --num 5 --user-id 1 --with-location
docker compose exec web python manage.py process_events
docker compose exec web python manage.py refresh_summaries
```

`USER_ID` is a Django user pk (the first superuser is usually `1`).

## Verification

- After Python changes: `make test` (or `make local-test` if that is the active setup).
- After changing a tagged region: tell the user the book listing will change; they need a matching commit in the book repo if they care about PDF/EPUB.
- After Compose/Make/settings changes: `make build && make dev` and hit `/analytics` (still N+1) and `/analytics_select_related`.
