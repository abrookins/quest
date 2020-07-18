.PHONY: clean dev test

dev:
		docker-compose up -d --build

test:	dev
		docker-compose run --rm test pytest

clean:
		docker-compose stop
		docker-compose rm -f
