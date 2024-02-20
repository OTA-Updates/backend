from device_group.models import DeviceGroup
from device_group.serializers import DeviceGroupSerializer

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class DeviceGroupListCreateView(ListCreateAPIView):
    queryset = DeviceGroup.objects.all()
    serializer_class = DeviceGroupSerializer


class DeviceGroupDetailView(RetrieveUpdateDestroyAPIView):
    queryset = DeviceGroup.objects.all()
    serializer_class = DeviceGroupSerializer
