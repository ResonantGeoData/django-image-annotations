"""Django REST Framework viewsets.

This module contains the DRF viewsets. These allow
easily routing serializers as resources.

https://www.django-rest-framework.org/api-guide/viewsets/
"""

from rest_framework import viewsets

from spatiotemporal.models import (
    Coverage,
    Measurement,
    Relationship,
    SpatialThing,
    Universe,
)
from spatiotemporal.serializers import (
    CoverageSerializer,
    MeasurementSerializer,
    RelationshipSerializer,
    SpatialThingSerializer,
    UniverseSerializer,
)


class UniverseViewSet(viewsets.ModelViewSet):
    queryset = Universe.objects.all()
    serializer_class = UniverseSerializer


class SpatialThingViewSet(viewsets.ModelViewSet):
    queryset = SpatialThing.objects.all()
    serializer_class = SpatialThingSerializer


class RelationshipViewSet(viewsets.ModelViewSet):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer


class CoverageViewSet(viewsets.ModelViewSet):
    queryset = Coverage.objects.all()
    serializer_class = CoverageSerializer


class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
