from device_group.views import DeviceGroupDetailView, DeviceGroupListCreateView

from django.urls import URLPattern, URLResolver, path


urlpatterns: list[URLPattern | URLResolver] = [
    path(
        "device-groups/",
        DeviceGroupListCreateView.as_view(),
        name="device-group-list-create",
    ),
    path(
        "device-groups/<int:pk>/",
        DeviceGroupDetailView.as_view(),
        name="device-group-detail",
    ),
]
