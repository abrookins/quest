from django.contrib.admin import AdminSite
from django.core.cache import cache
from django.db.models import Count, OuterRef, Subquery, IntegerField, Avg
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.urls import path

from goals.models import Goal, TaskStatus, GoalSummary
from quest import redis_key_schema

ONE_HOUR = 60 * 60


# tag::admin-site[]
class QuestAdminSite(AdminSite):
    def get_urls(self):
        urls = super().get_urls() + [
            path('goal_dashboard_python/',
                 self.admin_view(
                     self.goals_dashboard_view_py)),
            path('goal_dashboard_sql/',
                 self.admin_view(
                     self.goals_dashboard_view_sql)),
            path('goal_dashboard_materialized/',
                 self.admin_view(
                     self.goals_dashboard_view_materialized)),
            path('goal_dashboard_with_avg_completions/',
                 self.admin_view(
                     self.goals_avg_completions_view)),
            path('goal_dashboard_redis/',
                 self.admin_view(
                     self.goals_dashboard_view_redis))
        ]
        return urls
# end::admin-site[]

# tag::counting-with-python[]
    def goals_dashboard_view_py(self, request):
        """Render the top ten goals by completed tasks.

        WARNING: Don't do this! This example is of an
        anti-pattern: running an inefficient calculation in
        Python that you could offload to the database
        instead. See the goals_dashboard_view_sql() view
        instead.
        """
        goals = Goal.objects.all()

        for g in goals:  # <1>
            completions = TaskStatus.objects.completed()
            completed_tasks = completions.filter(
                task__in=g.tasks.values('id'))  # <2>
            setattr(g, 'completed_tasks',
                    completed_tasks.count())  # <3>

        goals = sorted(goals, key=lambda g: g.completed_tasks,
                       reverse=True)[:10]  # <4>

        return render(request, "admin/goal_dashboard.html",
                      {"goals": goals})
# end::counting-with-python[]

# tag::counting-with-sql[]
    def goals_dashboard_view_sql(self, request):
        completed_tasks = Subquery(  # <1>
            TaskStatus.objects.filter(
                task__goal=OuterRef('pk'),  # <2>
                status=TaskStatus.DONE
            ).values(
                'task__goal'
            ).annotate(  # <3>
                count=Count('pk')
            ).values('count'),
            output_field=IntegerField())  # <4>

        goals = Goal.objects.all().annotate(
            completed_tasks=Coalesce(completed_tasks, 0)
        ).order_by('-completed_tasks')[:10]

        return render(request, "admin/goal_dashboard.html",
                      {"goals": goals})
# end::counting-with-sql[]

# tag::caching-view-in-redis[]
    def goals_dashboard_view_redis(self, request):
        key = redis_key_schema.admin_goals_dashboard()
        cached_result = cache.get(key)

        if not cached_result:
            dashboard = self.goals_dashboard_view_sql(request)
            cache.set(key, dashboard, timeout=ONE_HOUR)
            return dashboard

        return cached_result
# end::caching-view-in-redis[]

# tag::aggregations[]
    def goals_avg_completions_view(self, request):
        completed_tasks = Subquery(
            TaskStatus.objects.filter(
                task__goal=OuterRef('pk'),
                status=TaskStatus.DONE
            ).values(
                'task__goal'
            ).annotate(
                count=Count('pk')
            ).values('count'),
            output_field=IntegerField())

        goals = Goal.objects.all().annotate(
            completed_tasks=Coalesce(completed_tasks, 0))
        top_ten_goals = goals.order_by('-completed_tasks')[:10]
        average_completions = goals.aggregate(
            Avg('completed_tasks'))  # <1>
        avg = int(average_completions['completed_tasks__avg'])

        other_stats = (
            {
                'name': 'Average Completed Tasks',
                'stat': avg
            },
        )
        return render(request, "admin/goal_dashboard.html", {
            "goals": top_ten_goals,
            "other_stats": other_stats
        })
# end::aggregations[]

# tag::querying-materialized-views[]
    def goals_dashboard_view_materialized(self, request):
        return render(request, "admin/goal_dashboard_materialized.html",
                      {"summaries": GoalSummary.objects.all().select_related()})
# end::querying-materialized-views[]


admin_site = QuestAdminSite()
