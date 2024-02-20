from device.models import Device

from rest_framework.serializers import ModelSerializer


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"
