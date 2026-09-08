COMPOSE ?= docker compose
PYTHON ?= .venv/bin/python
PORT ?= 8000
PG_BIN ?= /opt/homebrew/opt/postgresql@16/bin

.DEFAULT_GOAL := help

.PHONY: help build dev down logs shell migrate test superuser generate-events \
	runserver watch_static \
	local-setup local-check local-test local-run local-superuser local-generate-events

help:
	@echo "Quest — Docker is the default."
	@echo "  make build              build images"
	@echo "  make dev                Postgres, Redis, Django"
	@echo "  make test               pytest in Compose"
	@echo "  make superuser          createsuperuser in the web container"
	@echo "  make generate-events    NUM=500000 USER_ID=1"
	@echo "  make logs               follow web logs"
	@echo "  make down               stop the stack"
	@echo
	@echo "  http://127.0.0.1:$${QUEST_WEB_PORT:-8000}/"
	@echo "  Port busy? QUEST_WEB_PORT=8001 make dev"
	@echo
	@echo "Host venv (no Docker):"
	@echo "  make local-setup / local-test / local-run"

build:
	$(COMPOSE) build

dev:
	$(COMPOSE) up -d --build
	@echo "Quest is at http://127.0.0.1:$${QUEST_WEB_PORT:-8000}/"

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f web

shell:
	$(COMPOSE) exec web python manage.py shell

migrate:
	$(COMPOSE) exec web python manage.py migrate

test:
	$(COMPOSE) run --rm test

superuser:
	$(COMPOSE) exec web python manage.py createsuperuser

generate-events:
	$(COMPOSE) exec web python manage.py generate_events --num $(or $(NUM),500000) --user-id $(or $(USER_ID),1)

# Used as the web image command if you override Compose to `make runserver`.
runserver:
	python manage.py runserver 0.0.0.0:8000

watch_static:
	npm install && npm run watch

# --- host venv -------------------------------------------------------------

.venv/bin/python:
	uv venv --python 3.12 .venv
	uv pip install --python .venv/bin/python -r requirements.txt

local-setup: .venv/bin/python
	export PATH="$(PG_BIN):$$PATH"; \
	export QUEST_DATABASE_HOST=127.0.0.1 QUEST_DATABASE_PORT=5432 \
		QUEST_DATABASE_PASSWORD=test QUEST_REDIS_URL=redis://127.0.0.1:6379/0; \
	command -v psql >/dev/null || { echo "psql not found. brew install postgresql@16."; exit 1; }; \
	psql -h 127.0.0.1 -p 5432 -d postgres -tc "SELECT 1 FROM pg_roles WHERE rolname='quest'" | grep -q 1 || \
		psql -h 127.0.0.1 -p 5432 -d postgres -c "CREATE ROLE quest LOGIN PASSWORD 'test';"; \
	psql -h 127.0.0.1 -p 5432 -d postgres -tc "SELECT 1 FROM pg_database WHERE datname='quest'" | grep -q 1 || \
		psql -h 127.0.0.1 -p 5432 -d postgres -c "CREATE DATABASE quest OWNER quest;"; \
	$(PYTHON) manage.py migrate

local-check:
	export PATH="$(PG_BIN):$$PATH"; pg_isready -h 127.0.0.1 -p 5432
	redis-cli ping

local-test: .venv/bin/python
	QUEST_DATABASE_HOST=127.0.0.1 QUEST_REDIS_URL=redis://127.0.0.1:6379/0 \
		$(PYTHON) -m pytest

local-run: .venv/bin/python
	QUEST_DATABASE_HOST=127.0.0.1 QUEST_REDIS_URL=redis://127.0.0.1:6379/0 \
		$(PYTHON) manage.py runserver 127.0.0.1:$(PORT)

local-superuser: .venv/bin/python
	QUEST_DATABASE_HOST=127.0.0.1 QUEST_REDIS_URL=redis://127.0.0.1:6379/0 \
		$(PYTHON) manage.py createsuperuser

local-generate-events: .venv/bin/python
	QUEST_DATABASE_HOST=127.0.0.1 QUEST_REDIS_URL=redis://127.0.0.1:6379/0 \
		$(PYTHON) manage.py generate_events --num $(or $(NUM),500000) --user-id $(or $(USER_ID),1)
