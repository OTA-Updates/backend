from deployment_task.views import DeploymentTaskDestroyView, DeploymentTaskListView

from django.urls import URLPattern, URLResolver, path


urlpatterns: list[URLPattern | URLResolver] = [
    path(
        "deployment-tasks/",
        DeploymentTaskListView.as_view(),
        name="deployment-task-list-create",
    ),
    path(
        "deployment-tasks/<uuid:pk>/",
        DeploymentTaskDestroyView.as_view(),
        name="deployment-task-delete",
    ),
]
