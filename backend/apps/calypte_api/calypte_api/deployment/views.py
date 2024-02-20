from deployment.models import Deployment
from deployment.serializers import DeploymentSerializer

from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class DeploymentListCreateView(ListCreateAPIView):
    queryset = Deployment.objects.all()
    serializer_class = DeploymentSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class DeploymentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Deployment.objects.all()
    serializer_class = DeploymentSerializer
