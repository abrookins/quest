from django.shortcuts import render


def goals_list(request):
    return render(request, 'frontend/goals_list.html')
