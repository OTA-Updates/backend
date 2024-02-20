from device.views import DeviceDetailView, DeviceListCreateView

from django.urls import URLPattern, URLResolver, path


urlpatterns: list[URLPattern | URLResolver] = [
    path(
        "devices/",
        DeviceListCreateView.as_view(),
        name="device-list-create",
    ),
    path(
        "devices/<int:pk>/",
        DeviceDetailView.as_view(),
        name="device-detail",
    ),
]
