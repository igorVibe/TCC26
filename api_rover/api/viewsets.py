from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api_rover.models import Rover, Telemetria
from api_rover.api.serializers import RoverSerializer, TelemetriaSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RoverViewSet(viewsets.ModelViewSet):
    queryset = Rover.objects.all()
    serializer_class = RoverSerializer
    permission_classes = [IsAuthenticated]


class TelemetriaViewSet(viewsets.ModelViewSet):
    queryset = Telemetria.objects.all().order_by('-data_hora')
    serializer_class = TelemetriaSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'rover',
                openapi.IN_QUERY,
                description='ID do Rover para filtrar as telemetrias. Ex: ROVER-01',
                type=openapi.TYPE_STRING,
                required=False
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Telemetria.objects.all().order_by('-data_hora')
        rover_id = self.request.query_params.get('rover')

        if rover_id:
            queryset = queryset.filter(rover_id=rover_id)

        return queryset