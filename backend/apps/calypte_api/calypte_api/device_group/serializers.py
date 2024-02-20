from device_group.models import DeviceGroup

from rest_framework.serializers import ModelSerializer


class DeviceGroupSerializer(ModelSerializer):
    class Meta:
        model = DeviceGroup
        fields = "__all__"
