from django.views.generic import ListView, CreateView

from goals.models import Goal


class GoalList(ListView):
    """Display a list of Goals"""
    model = Goal
    template_name = "goals/goal_list.html"
    context_object_name = "goals"


class GoalCreate(CreateView):
    """Display a Goal creation form"""
    model = Goal
    fields = ('name',)
    template_name = "goals/goal_create.html"
    context_object_name = "goals"
    success_url = "/goals"
