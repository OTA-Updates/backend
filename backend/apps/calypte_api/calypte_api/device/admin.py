from device.models import Device

from django.contrib import admin


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "group",
        "serial_number",
        "firmware",
        "last_seen",
        "registration_date",
        "created_at",
        "updated_at",
    )
