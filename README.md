# Quest LMS

This is the example application for the 2nd Edition of the book [The Temple of Django Database Performance](https://spellbookpress.com).

## Note: Unreleased Content!

This project is for the _second_ edition of the book, which as of 8/2020 is not yet published.

**Note**: Not sure which one you have? The first edition has a white cover, and the second edition a black cover.

## Setup

Run `create_database.sql` with a user that has psql access (e.g., `postgres`):

  psql -f create_database.sql

Install dependencies:

  pip install -f requirements.txt

## Development

The Makefile houses `make` shortcuts for all development tasks.

You should build Docker images for the project locally before anything else:

    make build
    
Then start the project's app and databases:

    make dev
