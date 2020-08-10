# Database Performance Tips with Django

## Intro [4 mins]
* Me
    * Redis for Python Developers course August 18, sign up now, free
    * The Temple of Django Database Performance
* Quest app
    * Quest Learning Management System
    * Postgres
    * Redis
* PyCharm

## Querying [15 mins]
* Pagination
    * Before -- http://localhost:8000/analytics
    * Look at code: .all() all items
    * Open DB console and get # of items in table
    * Use pagination (offset) http://localhost:8000/analytics_offset
    * Debug Toolbar - # of queries, speed
    * Add select_related()
    * Preview: Keyset Pagination
        * Explain why you would need this (Offset pagination breaks)
        * CursorPagination with DRF - 3 mins
        * Refer to book for more
* Annotations
    * What is an annotation?
    * Counting with Python - http://localhost:8000/admin/goal_dashboard_sql/
    * Counting with SQL/Annotations - http://localhost:8000/admin/goal_dashboard_sql/
* Materialized Views
    * Explanation - like caching in the database
    * Code [model for materialized view, code for migration]
    * Run the migration
    * View http://localhost:8000/admin/goal_dashboard_materialized/
    * Show refresh_summaries management command

## Indexing [15 mins]
* Covering indexes
    * What this is and how it works
    * Show queries in database panel
    * First we need to add an index… let’s do it concurrently in PG
    * AddIndexConcurrently in Django 3
    * Explanation (building indexes locks tables, concurrently doesn’t)
    * Show analytics migrations 0009 and 0010 
    * Explain analyze query without index - Database Panel
    * Run migration
    * Explain analyze query with index - Database Panel
    * Should be index query
    * May NOT be covering/index-only yet
    * VACUUM if needed
    * Run query again - should be index only
 * Partial indexes
     * Difference compared to regular index
        * Use to EXCLUDE common data from the index (better write perf, smaller index)
     * Show analytics index
     * Show analytics migrations 0012
     * Run migration
     * VACUUM 
     * Run query again - should be index only
   

## Caching and Redis [15]
* Using the caching framework
    * Why redis? The swiss-army knife of databases
    * Code [Settings.py - turn on caching with redis]
    * Show middleware - will cache entire site in redis
    * Admin dashboard Redis version -- caching the calculated values in Redis
* Session storage with Redis
    * Explanation
    * Code [settings.py]
    * Demo: log in, examine redis keys with database tool in PyCharm
* Custom auth backend for token storage in Redis with DRF
    * Explanation [looking up auth tokens is slow, use redis]
    * Code [custom auth backend]
    * Create a token in redis-cli
    * Check that we can authenticate using the token

## Q&A [10]
* Any questions?
