from deployment.views import DeploymentDetailView, DeploymentListCreateView

from django.urls import URLPattern, URLResolver, path


urlpatterns: list[URLPattern | URLResolver] = [
    path(
        "deployments/",
        DeploymentListCreateView.as_view(),
        name="deployment-list-create",
    ),
    path(
        "deployments/<int:pk>/",
        DeploymentDetailView.as_view(),
        name="deployment-detail",
    ),
]
