from quest.admin import admin_site

from .models import Goal, Task, TaskStatus

admin_site.register(Goal)
admin_site.register(Task)
admin_site.register(TaskStatus)
