import pytest
from django.contrib.auth.models import User
from django.urls.base import reverse

TEST_PASSWORD = "password"


@pytest.fixture
def user():
    return User.objects.create_user(
        username="Mac", password=TEST_PASSWORD)


@pytest.fixture
def authenticated_client(user, client):
    client.login(username=user.username, password=TEST_PASSWORD)
    return client


@pytest.mark.django_db
def test_get_task(authenticated_client):
    url = reverse("task", kwargs={"pk":1})
    resp = authenticated_client.get(url)
    assert resp['status'] == 'ok'

