from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def goals_list(request):
    return render(request, 'frontend/goals_list.html')


@login_required
def goal_detail(request, pk):
    return render(request, 'frontend/goal.html', {
        "goal_id": pk
    })
