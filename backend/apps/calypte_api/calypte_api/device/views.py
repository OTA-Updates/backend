from device.models import Device
from device.serializers import DeviceSerializer

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class DeviceListCreateView(ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


# Create your views here.
