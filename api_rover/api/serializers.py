from rest_framework import serializers
from api_rover.models import Rover, Telemetria

class RoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rover
        fields = '__all__'

class TelemetriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telemetria
        fields = '__all__'