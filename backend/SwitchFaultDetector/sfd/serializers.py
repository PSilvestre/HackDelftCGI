from rest_framework import serializers
from .models import SwitchModel


class SwitchModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwitchModel
        fields = ('switch_id', 'timestamp', 'description', 'file_name')