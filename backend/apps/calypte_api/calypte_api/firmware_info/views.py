from firmware_info.models import FirmwareInfo
from firmware_info.serializers import FirmwareInfoSerializer

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class FirmwareInfoListCreateView(ListCreateAPIView):
    queryset = FirmwareInfo.objects.all()
    serializer_class = FirmwareInfoSerializer


class FirmwareInfoDetailView(RetrieveUpdateDestroyAPIView):
    queryset = FirmwareInfo.objects.all()
    serializer_class = FirmwareInfoSerializer
