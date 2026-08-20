from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api_rover.models import Rover, Telemetria
from api_rover.api.serializers import RoverSerializer, TelemetriaSerializer


class RoverViewSet(viewsets.ModelViewSet):
    queryset = Rover.objects.all()
    serializer_class = RoverSerializer
    permission_classes = [IsAuthenticated]


class TelemetriaViewSet(viewsets.ModelViewSet):
    queryset = Telemetria.objects.all().order_by('-data_hora')
    serializer_class = TelemetriaSerializer
    permission_classes = [IsAuthenticated]