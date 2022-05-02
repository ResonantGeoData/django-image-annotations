"""Django REST Framework viewsets.

This module contains the DRF viewsets. These allow
easily routing serializers as resources.

https://www.django-rest-framework.org/api-guide/viewsets/
"""

from rest_framework import viewsets

from spatiotemporal.models import (
    Coverage,
    Measurement,
    SpatialThing,
    TimeUnit,
    Universe,
)
from spatiotemporal.serializers import (
    CoverageSerializer,
    MeasurementSerializer,
    SpatialThingSerializer,
    TimeUnitSerializer,
    UniverseSerializer,
)


class TimeUnitViewSet(viewsets.ModelViewSet):
    queryset = TimeUnit.objects.all()
    serializer_class = TimeUnitSerializer


class UniverseViewSet(viewsets.ModelViewSet):
    queryset = Universe.objects.all()
    serializer_class = UniverseSerializer


class SpatialThingViewSet(viewsets.ModelViewSet):
    queryset = SpatialThing.objects.all()
    serializer_class = SpatialThingSerializer


class CoverageViewSet(viewsets.ModelViewSet):
    queryset = Coverage.objects.all()
    serializer_class = CoverageSerializer


class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
