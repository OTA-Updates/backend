from device_group.models import DeviceGroup

from django.contrib import admin


@admin.register(DeviceGroup)
class DeviceGroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "protocol",
        "shared_secret",
        "created_at",
        "updated_at",
    )
