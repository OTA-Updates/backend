from protocol.models import Protocol

from django.contrib import admin


@admin.register(Protocol)
class ProtocolAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
