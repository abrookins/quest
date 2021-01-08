import pytest
from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse

from analytics.models import Event
from analytics.views import encode_keyset, JsonbFieldIncrementer

TEST_PASSWORD = "password"


# tag::fixtures[]
@pytest.fixture
def user():
    return User.objects.create_user(
        username="Mac", password=TEST_PASSWORD)


@pytest.fixture
def events(user):
    Event.objects.create(
        name="goal.viewed", user=user, data={"test": 1})
    Event.objects.create(
        name="goal.clicked", user=user, data={"test": 2})
    Event.objects.create(
        name="goal.favorited", user=user, data={"test": 3})
    return Event.objects.all().order_by('pk')


# end::fixtures[]

@pytest.fixture
def authenticated_client(user, client):
    client.login(username=user.username, password=TEST_PASSWORD)
    return client


@pytest.fixture
@override_settings(DEBUG=True, EVENTS_PER_PAGE=2)
def page_one_generic(authenticated_client):
    url = reverse("events_keyset_generic")
    return authenticated_client.get(url)


@pytest.fixture
@override_settings(DEBUG=True, EVENTS_PER_PAGE=2)
def page_one_pg(authenticated_client):
    url = reverse("events_keyset_pg")
    return authenticated_client.get(url)


def content(page):
    return page.content.decode("utf-8")


@pytest.mark.django_db
def test_includes_page_one_results(events, page_one_generic):
    assert events[0].name in content(page_one_generic)
    assert events[1].name in content(page_one_generic)


@pytest.mark.django_db
def test_hides_second_page_results(events, page_one_generic):
    assert events[2].name not in content(page_one_generic)


@pytest.mark.django_db
def test_has_next_link(events, page_one_generic):
    last_page_one_event = events[1]
    expected_keyset = encode_keyset(last_page_one_event)
    assert expected_keyset in content(page_one_generic)


@pytest.mark.django_db
def test_next_link_requests_next_page(events, page_one_generic,
                                      authenticated_client):
    next_keyset = page_one_generic.context['next_keyset']
    next_page_url = "{}?keyset={}".format(
        reverse("events_keyset_generic"), next_keyset)
    page_two_event = events[2]
    page_two = authenticated_client.get(next_page_url)
    assert page_two_event.name in content(page_two)


@pytest.mark.django_db
def test_includes_page_one_results_pg(events, page_one_pg):
    assert events[0].name in content(page_one_pg)
    assert events[1].name in content(page_one_pg)


@pytest.mark.django_db
def test_hides_second_page_results_pg(events, page_one_pg):
    assert events[2].name not in content(page_one_pg)


@pytest.mark.django_db
def test_has_next_link_pg(events, page_one_pg):
    last_page_one_event = events[1]
    expected_keyset = encode_keyset(last_page_one_event)
    assert expected_keyset in content(page_one_pg)


@pytest.mark.django_db
def test_next_link_requests_next_page_pg(events, page_one_pg,
                                         authenticated_client):
    next_keyset = page_one_pg.context['next_keyset']
    next_page_url = "{}?keyset={}".format(
        reverse("events_keyset_pg"), next_keyset)
    page_two_event = events[2]
    page_two = authenticated_client.get(next_page_url)
    assert page_two_event.name in content(page_two)


# tag::testing_jsonb_incrementer[]
@pytest.mark.django_db
def test_json_incrementer_sets_missing_count(events):
    assert all(['count' not in e.data for e in events])
    incr_by_one = JsonbFieldIncrementer('data', 'count', 1)
    events.update(data=incr_by_one)
    for event in events:
        assert event.data['count'] == 1


@pytest.mark.django_db
def test_json_incrementer_increments_count(events):
    events.update(data={"count": 1})
    incr_by_one = JsonbFieldIncrementer('data', 'count', 1)
    events.update(data=incr_by_one)
    for event in events:
        assert event.data['count'] == 2
# end::testing_jsonb_incrementer[]
