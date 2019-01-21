from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def goals_list(request):
    """Render the goals list page"""
    return render(request, 'frontend/goals_list.html')


@login_required
def goal_detail(request, pk):
    """Render the goal page for an existing goal"""
    return render(request, 'frontend/goal.html', {
        "goal_id": pk
    })


@login_required
def new_goal(request):
    """Render the new goal form page"""
    return render(request, 'frontend/new_goal.html')
