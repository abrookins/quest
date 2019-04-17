from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from analytics.models import Event


@login_required
def events(request):
    """Render the list of analytics events"""
    evs = Event.objects.all().select_related('user', 'user__profile',
                                             'user__profile__account')
    context = {'events': evs}
    return render(request, "analytics/events.html", context)
