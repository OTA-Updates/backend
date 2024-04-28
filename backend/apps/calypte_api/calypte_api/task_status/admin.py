from task_status.models import TaskStatus

from django.contrib import admin


# Register your models here.
@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "state", "created_at", "updated_at")
