import base64
import binascii
import datetime
import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F, Func, Value
from django.db.models.expressions import RawSQL
from django.http import HttpResponseBadRequest
from django.shortcuts import render

from analytics.models import Event

log = logging.getLogger(__name__)


@login_required
def all_events(request):
    """Render the list of analytics events."""
    events = Event.objects.all()
    context = {'events': events}
    return render(request, "analytics/events.html", context)


# tag::unpaginated[]
@login_required
def events_select_related(request):
    """Render the list of analytics events using select_related()."""
    events = Event.objects.all().select_related(
        'user', 'user__profile',
        'user__profile__account')
    context = {'events': events}
    return render(request, "analytics/events.html", context)
# end::unpaginated[]


# tag::paginated[]
@login_required
def events_offset_paginated(request):
    """Render the list of analytics events.

    Paginate results using Paginator, with select_related().
    """
    events = Event.objects.all().select_related(
        'user', 'user__profile',
        'user__profile__account').order_by('id')  # <1>
    paginated = Paginator(events, settings.EVENTS_PER_PAGE)
    page = request.GET.get('page', 1)
    events = paginated.get_page(page)
    context = {'events': events}
    return render(request, "analytics/events_paginated.html",
                  context)
# end::paginated[]


# tag::keyset_pagination_pg[]
KEYSET_SEPARATOR = '-'


class KeysetError(Exception):
    pass


def encode_keyset(last_in_page):
    """Return a URL-safe base64-encoded keyset."""
    return base64.urlsafe_b64encode(  # <1>
        "{}{}{}".format(
            last_in_page.pk,
            KEYSET_SEPARATOR,
            last_in_page.created_at.timestamp()
        ).encode(
            "utf-8"
        )
    ).decode("utf-8")


def decode_keyset(keyset):
    """Decode a base64-encoded keyset URL parameter."""
    try:
        keyset_decoded = base64.urlsafe_b64decode(
            keyset).decode("utf-8")
    except (AttributeError, binascii.Error):  # <2>
        log.debug("Could not base64-decode keyset: %s",
                  keyset)
        raise KeysetError
    try:
        pk, created_at_timestamp = keyset_decoded.split(
            KEYSET_SEPARATOR)
    except ValueError:
        log.debug("Invalid keyset: %s", keyset)
        raise KeysetError
    try:
        created_at = datetime.datetime.fromtimestamp(
            float(created_at_timestamp))
    except (ValueError, OverflowError):
        log.debug("Could not parse created_at timestamp "
                  "from keyset: %s", created_at_timestamp)
        raise KeysetError

    return pk, created_at


@login_required
def events_keyset_paginated_postgres(request):
    """Render the list of analytics events.

    Paginates results using the "keyset" method. This
    approach uses the row comparison feature of Postgres and
    is thus Postgres-specific. However, note that the latest
    versions of MySQL and SQLite also support row
    comparisons.

    The client should pass a "keyset" parameter that
    contains the set of values used to produce a stable
    ordering of the data. The values should be appended to
    each other and separated by a period (".").
    """
    keyset = request.GET.get('keyset')
    next_keyset = None

    if keyset:
        try:
            pk, created_at = decode_keyset(keyset)
        except KeysetError:
            return HttpResponseBadRequest(
                "Invalid keyset specified")

        events = Event.objects.raw("""
            SELECT *
            FROM analytics_event
            LEFT OUTER JOIN "auth_user"
              ON ("analytics_event"."user_id" = "auth_user"."id")
            LEFT OUTER JOIN "accounts_userprofile"
              ON ("auth_user"."id" = "accounts_userprofile"."user_id")
            LEFT OUTER JOIN "accounts_account"
              ON ("accounts_userprofile"."account_id" = "accounts_account"."id")
            WHERE (created_at, id) > (%s::timestamptz, %s)  -- <3>
            ORDER BY created_at, id  -- <4>
            FETCH FIRST %s ROWS ONLY
        """, [created_at.isoformat(), pk,
              settings.EVENTS_PER_PAGE])
    else:
        events = Event.objects.all().order_by(
            'created_at', 'pk').select_related(
            'user', 'user__profile',
            'user__profile__account')

    page = events[:settings.EVENTS_PER_PAGE]  # <5>
    if page:
        last_item = page[len(page) - 1]
        next_keyset = encode_keyset(last_item)

    context = {
        'events': page,
        'next_keyset': next_keyset
    }

    return render(
        request,
        "analytics/events_keyset_pagination.html",
        context)
# end::keyset_pagination_pg[]


# tag::keyset_pagination_generic[]
@login_required
def events_keyset_paginated_generic(request):
    """Render the list of analytics events.

    Paginates results using the "keyset" method. Instead of
    row comparisons, this implementation uses a generic
    boolean logic approach to building the keyset query.

    The client should pass a "keyset" parameter that
    contains the set of values used to produce a stable
    ordering of the data. The values should be appended to
    each other and separated by a period (".").
    """
    keyset = request.GET.get('keyset')
    events = Event.objects.all().order_by(
        'created_at', 'pk').select_related(
        'user', 'user__profile',
        'user__profile__account')
    next_keyset = None

    if keyset:
        try:
            pk, created_at = decode_keyset(keyset)
        except KeysetError:
            return HttpResponseBadRequest(
                "Invalid keyset specified")

        events.filter(  # <1>
            created_at__gte=created_at
        ).exclude(
            created_at=created_at,
            pk__lte=pk
        )

    page = events[:settings.EVENTS_PER_PAGE]
    if page:
        last_item = page[len(page) - 1]
        next_keyset = encode_keyset(last_item)

    context = {
        'events': page,
        'next_keyset': next_keyset
    }

    return render(
        request,
        "analytics/events_keyset_pagination.html",
        context)
# end::keyset_pagination_generic[]


# tag::increment_all_event_versions[]
@login_required
def increment_all_event_versions():
    """Increment all event versions in the database.

    Looping over each event and calling save() generates
    a query per event. That could mean a TON of queries!
    """
    for event in Event.objects.all():
        event.version = event.version + 1
        event.save()
# end::increment_all_event_versions[]


# tag::increment_all_event_versions_f_expression[]
@login_required
def increment_all_event_versions_with_f_expression():
    """Increment all event versions in the database.

    An F() expression can use a single query to update
    potentially millions of rows.
    """
    Event.objects.all().update(version=F('version') + 1)
# end::increment_all_event_versions_f_expression[]


# tag::update_all_events[]
@login_required
def increment_all_event_counts():
    """Update all event counts in the database."""
    for event in Event.objects.all():
        if 'count' in event.data:
            event.data['count'] += event.data['count']
        else:
            event.data['count'] = 1
        event.save()
# end::update_all_events[]


# tag::update_all_events_func[]
class JsonbFieldIncrementer(Func):  # <1>
    """Set or increment a property of a JSONB column."""
    function = "jsonb_set"
    arity = 3

    def __init__(self, json_column, property_name,
                 increment_by, **extra):
        property_expression = Value("{{{}}}".format
                                    (property_name))  # <2>
        set_or_increment_expression = RawSQL(  # <3>
            "(COALESCE({}->>'{}','0')::int + %s)" \
            "::text::jsonb".format(  # <4>
                json_column, property_name
            ), (increment_by,))

        super().__init__(json_column, property_expression,
                         set_or_increment_expression, **extra)


@login_required
def increment_all_event_counts_with_func():
    """Increment all event counts."""
    incr_by_one = JsonbFieldIncrementer('data', 'count', 1)
    Event.objects.all().update(data=incr_by_one).limit(10)
# end::update_all_events_func[]
