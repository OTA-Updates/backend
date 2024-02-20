from task_log_record.models import TaskLogRecord

from django.contrib import admin


@admin.register(TaskLogRecord)
class TaskLogRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "task",
        "created_at",
        "updated_at",
    )
