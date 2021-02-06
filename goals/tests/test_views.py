import pytest
from django.core.cache import cache
from django.contrib.auth.models import User
from django.urls.base import reverse

from goals.models import Goal, Task
from quest.connections import redis_connection
from quest import redis_key_schema


TEST_PASSWORD = "password"


@pytest.fixture
def redis():
    conn = redis_connection()
    yield conn

    # Delete test keys from redis after a test run.
    for key in conn.scan_iter(f"{redis_key_schema.PREFIX}:*"):
        conn.delete(key)



@pytest.fixture
def user():
    yield User.objects.create_user(
        username="Mac", password=TEST_PASSWORD)


@pytest.fixture
def task(user):
    goal = Goal.objects.create(name="Learn Django", user=user)
    task = Task.objects.create(goal=goal, name="Read caching docs")
    yield task


@pytest.fixture
def authenticated_client(user, client):
    client.login(username=user.username, password=TEST_PASSWORD)
    yield client


@pytest.mark.django_db
def test_get_task(authenticated_client, task):
    url = reverse("task", kwargs={"uuid": task.uuid})
    resp = authenticated_client.get(url)
    assert resp.json() == {'id': task.id, 'name': 'Read caching docs', 'goal': task.goal.id, 'completed': False}


@pytest.mark.django_db
def test_get_task_uses_cache(authenticated_client, task, redis):
    url = reverse("task", kwargs={"uuid": task.uuid})
    authenticated_client.get(url)
    cached_task = cache.get(redis_key_schema.task(task.uuid))
    assert cached_task == {'completed': False, 'goal': 2, 'id': 2, 'name': 'Read caching docs'}

