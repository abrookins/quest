from django.shortcuts import render


def goals_list(request):
    return render(request, 'frontend/goals_list.html')


def goal_detail(request, pk):
    return render(request, 'frontend/goal.html', {
        "goal_id": pk
    })
