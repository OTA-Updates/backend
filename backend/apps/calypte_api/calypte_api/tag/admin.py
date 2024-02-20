from tag.models import Tag

from django.contrib import admin


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "color",
        "group",
        "created_at",
        "updated_at",
    )
