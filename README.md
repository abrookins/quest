# quest

This is the example code for the book [The Temple of Django Database Performance](https://spellbookpress.com/books/temple-of-django-database-performance/) by Andrew Brookins.

## A Note on Versions

This code is for version 2 of the book, published August 2020. All buyers of the version 1 ebook (2019) have access to version 2 as a free download.

If you purchased the 2019 edition of the print book, this code is not substantially different than the code referenced in that book. However, this code includes a new example on using materialized views.

## Setup

This project uses Docker to set up its environment, and it includes a Makefile to let you run `docker-compose` commands more easily.

### Initial Setup

Run `make build` to build the images for the environment.

You'll also want to run `docker-compose run web ./manage.py createsuperuser` to create a superuser for yourself.

### Dev Server

Run `make dev` to run Redis, Postgres, and the Django web application. The example's servers bind their ports to localhost, so you can visit the app at https://localhost:8000 once it's running.

## Viewing Logs

Run `docker-compose logs web` to view logs for the web application. Likewise, 'postgres' and 'redis' will show logs for those servers.

## Running Tests

Run `make test` to run the tests. Tests run in a container. If you drop in "import ipdb; ipdb.set_trace()" anywhere in the project code, you'll drop into a debugging session if the tests hit that code.

## Generating Data for Performance Problems

Recreating many of the performance problems in this book requires a large amount of data in your database. This project includes a management command that will generate analytics events sufficient to cause performance problems.

Here's an example of using the management command to generate 500,000 analytics events for the user with
ID 1 (in my case, this is my admin user):

    $ docker-compose run web ./manage.py generate_events --num 500000 --user-id 1

## Copyright

This example code is copyright 2020 Andrew Brookins.
