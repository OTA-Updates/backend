from firmware_info.models import FirmwareInfo

from rest_framework.serializers import ModelSerializer


class FirmwareInfoSerializer(ModelSerializer):
    class Meta:
        model = FirmwareInfo
        fields = "__all__"
