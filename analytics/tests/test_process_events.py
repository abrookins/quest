import datetime
from io import StringIO
from unittest.mock import Mock, patch

import pytest
from django.core.management import call_command

from analytics.management.commands.process_events import cloud_cover_at
from analytics.models import Event


@patch("analytics.management.commands.process_events.requests.get")
def test_cloud_cover_at_picks_the_event_hour(mock_get):
    cloud_cover = [0] * 24
    cloud_cover[15] = 41
    mock_get.return_value = Mock(
        **{"json.return_value": {"hourly": {"cloud_cover": cloud_cover}}}
    )
    mock_get.return_value.raise_for_status = Mock()

    when = datetime.datetime(2019, 9, 25, 15, 30, tzinfo=datetime.timezone.utc)
    assert cloud_cover_at(44.52, -123.0, when) == 41

    params = mock_get.call_args.kwargs["params"]
    assert params["start_date"] == "2019-09-25"
    assert params["hourly"] == "cloud_cover"
    assert params["timezone"] == "UTC"


@pytest.mark.django_db
def test_generate_events_omits_location_by_default():
    call_command("generate_events", num=1, stdout=StringIO())
    assert "latitude" not in Event.objects.get().data


@pytest.mark.django_db
def test_generate_events_with_location_sets_coordinates():
    call_command("generate_events", num=1, with_location=True, stdout=StringIO())
    data = Event.objects.get().data
    assert data["latitude"] == 44.523064
    assert data["longitude"] == -123.258


@pytest.mark.django_db
def test_process_events_reports_when_nothing_has_coordinates():
    call_command("generate_events", num=1, stdout=StringIO())
    out = StringIO()
    call_command("process_events", stdout=out)
    assert "No events had latitude/longitude" in out.getvalue()
