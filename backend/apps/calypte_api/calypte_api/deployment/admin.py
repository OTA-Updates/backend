from deployment.models import Deployment

from django.contrib import admin


@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "group",
        "firmware",
        "scheduled_date",
        "completion_date",
        "created_at",
        "updated_at",
    )
