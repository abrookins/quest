from goals.models import Goal, Task
import pytest
from django.contrib.auth.models import User
from django.urls.base import reverse

TEST_PASSWORD = "password"


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
    url = reverse("task", kwargs={"pk": task.pk})
    resp = authenticated_client.get(url)
    assert resp.json() == {'id': task.id, 'name': 'Read caching docs', 'goal': task.goal.id, 'completed': False}
