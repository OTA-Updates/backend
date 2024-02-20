from deployment_task.models import DeploymentTask
from deployment_task.serializers import DeploymentTaskSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import DestroyAPIView, ListAPIView


class DeploymentTaskListView(ListAPIView):
    queryset = DeploymentTask.objects.all()
    serializer_class = DeploymentTaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["deployment"]


class DeploymentTaskDestroyView(DestroyAPIView):
    queryset = DeploymentTask.objects.all()
    serializer_class = DeploymentTaskSerializer
