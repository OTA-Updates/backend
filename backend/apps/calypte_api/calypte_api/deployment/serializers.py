from uuid import UUID

from deployment.models import Deployment

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class DeploymentSerializer(ModelSerializer):
    state = serializers.SerializerMethodField(
        method_name="get_state_display", read_only=True
    )
    devices = serializers.ListField(write_only=True, required=True)

    # TODO: Implement get_state_display
    def get_deployment_state(self, queryset: Deployment) -> str:
        return "TODO: Implement get_state_display"

    # TODO: Implement validate_devices
    def validate_devices(self, devices: list[UUID]) -> list[UUID]:
        return devices

    class Meta:
        model = Deployment
        fields = "__all__"
