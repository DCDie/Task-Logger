Milestone 4
In this milestone we start to improve our application.

~~1. Add unit tests for each endpoint https://www.django-rest-framework.org/api-guide/testing/~~
~~2. Add coverage package and generate report to be sure in 100% test coverage https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#integration-with-coverage-py~~
~~3. Install PostgreSQL docker container and move your app on PostgreSQL (edit settings.py)~~
~~4. Create a script that will add random 25.000 tasks and 50.000 time logs~~
~~5. Install PGHero docker container and connect it to your db https://github.com/ankane/pghero/blob/master/guides/Docker.md~~
~~6. Manual test all endpoints and check with PGHero that all sql queries use db indexes~~
7. Install Redis docker container and configure Django to cache with 1 minute TTL the endpoint with Top 20 tasks by time for each user https://github.com/jazzband/django-redis
8. Create Dockerfile for your application to run it with docker-compose command