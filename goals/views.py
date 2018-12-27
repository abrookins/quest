from django.views.generic import ListView

from goals.models import Goal


class GoalList(ListView):
    """Display a list of Goals"""
    model = Goal
    template_name = "goals/goal_list.html"
    context_object_name = "goals"

