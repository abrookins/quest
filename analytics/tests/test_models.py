from django.db import connection, reset_queries
from django.contrib.auth.models import User
from django.test import override_settings
import pytest

from analytics.models import Event


# tag::fixtures[]
@pytest.fixture
def user():
    return User.objects.create_user(username="Mac", password="Daddy")


@pytest.fixture
def events(user):  # <1>
    Event.objects.create(name="goal.viewed", user=user, data="{test:1}")
    Event.objects.create(name="goal.viewed", user=user, data="{test:2}")


# end::fixtures[]

# tag::test_only[]
@override_settings(DEBUG=True)
@pytest.mark.django_db
def test_only(events):
    reset_queries()
    event_with_data = Event.objects.first()
    assert event_with_data.data == "{test:1}"
    assert len(connection.queries) == 1  # <2>

    event_without_data = Event.objects.only('name').first()
    assert event_without_data.data == "{test:1}"
    assert event_without_data.name == "goal.viewed"
    assert len(connection.queries) == 3  # <3>
# end::test_only[]


# tag::test_only_with_relations[]
@override_settings(DEBUG=True)
@pytest.mark.django_db
def test_only_with_relations(events):
    reset_queries()
    e = Event.objects.select_related('user').only('user').first()  # <1>
    assert len(connection.queries) == 1

    assert e.name == 'goal.viewed'
    assert len(connection.queries) == 2  # <2>

    assert e.user.username == 'Mac'
    assert len(connection.queries) == 2  # <3>
# end::test_only_with_relations[]


# tag::test_defer[]
@override_settings(DEBUG=True)
@pytest.mark.django_db
def test_defer(events):
    reset_queries()
    event_with_data = Event.objects.first()
    assert event_with_data.data == "{test:1}"
    assert len(connection.queries) == 1

    event_without_data = Event.objects.defer('data').first()  # <1>
    assert event_without_data.data == "{test:1}"
    assert len(connection.queries) == 3
# end::test_defer[]
