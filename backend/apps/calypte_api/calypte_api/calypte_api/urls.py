"""
URL configuration for calypte_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from calypte_api import settings

from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path


API_VERSION = "v1"

urlpatterns: list[URLPattern | URLResolver] = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/auth/",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
    path("api/v1/", include("deployment.urls"), name="deployment"),
    path("api/v1/", include("deployment_task.urls"), name="deployment_task"),
    path("api/v1/", include("device.urls"), name="device"),
    path("api/v1/", include("device_group.urls"), name="device_group"),
    path("api/v1/", include("firmware_file.urls"), name="firmware_file"),
    path("api/v1/", include("firmware_info.urls"), name="firmware_info"),
    path("api/v1/", include("task_log_record.urls"), name="task_log_record"),
    path("api/v1/", include("tag.urls"), name="tag"),
    path("api/v1/", include("calypte_user.urls"), name="user"),
]

if settings.DEBUG:
    import debug_toolbar  # type: ignore

    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view
    from rest_framework import permissions

    schema_view = get_schema_view(
        openapi.Info(
            title="calypte API",
            default_version="v1",
            description="Provides code documents",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="zigman.nikita@gmail.com"),
            license=openapi.License(name="GNU GENERAL PUBLIC LICENSE"),
        ),
        public=False,
        permission_classes=[
            permissions.AllowAny,
        ],
    )

    urlpatterns.extend(
        [
            path(
                "docs/",
                schema_view.with_ui("swagger", cache_timeout=0),
                name="schema-swagger-ui",
            ),
            path("__debug__/", include(debug_toolbar.urls)),
        ]
    )
