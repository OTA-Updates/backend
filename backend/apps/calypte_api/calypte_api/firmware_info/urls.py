from firmware_info.views import FirmwareInfoDetailView, FirmwareInfoListCreateView

from django.urls import URLPattern, URLResolver, path


urlpatterns: list[URLPattern | URLResolver] = [
    path(
        "firmware-info/",
        FirmwareInfoListCreateView.as_view(),
        name="firmware-info-list-create",
    ),
    path(
        "firmware-info/<int:pk>/",
        FirmwareInfoDetailView.as_view(),
        name="firmware-info-detail",
    ),
]
