from firmware_info.models import FirmwareInfo

from django.contrib import admin


@admin.register(FirmwareInfo)
class FirmwareInfoAdmin(admin.ModelAdmin):
    list_display = (
        "version",
        "group",
        "serial_number",
        "created_at",
        "updated_at",
    )
