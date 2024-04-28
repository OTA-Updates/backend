from deployment_task.models import DeploymentTask

from django.contrib import admin


@admin.register(DeploymentTask)
class DeploymentTaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "deployment",
        "device",
        "state",
        "created_at",
        "updated_at",
    )
