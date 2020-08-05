.PHONY: clean dev test

build:
		docker-compose build

dev:
		docker-compose up -d

shell:
		docker-compose exec web ./manage.py shell

migrate:
		docker-compose exec web ./manage.py migrate

test:	dev
		docker-compose run --rm test pytest

clean:
		docker-compose stop
		docker-compose rm -f

watch_static:
		npm install && npm run watch

runserver:
		python manage.py runserver 0.0.0.0:8000
