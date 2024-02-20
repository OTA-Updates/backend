from deployment_task.models import DeploymentTask

from rest_framework.serializers import ModelSerializer


class DeploymentTaskSerializer(ModelSerializer):
    class Meta:
        model = DeploymentTask
        fields = "__all__"
        depth = 2
