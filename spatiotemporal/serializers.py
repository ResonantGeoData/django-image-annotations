"""Django REST Framework serializers.

This module contains the DRF serializers. These allow
manipulating the Django models represented by JSON.

https://www.django-rest-framework.org/api-guide/serializers/
"""

from rest_framework import serializers

from spatiotemporal.models import (
    Coverage,
    Measurement,
    Relationship,
    SpatialThing,
    Universe,
)


class UniverseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Universe
        fields = "__all__"


class SpatialThingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpatialThing
        fields = "__all__"


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = "__all__"


class CoverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coverage
        fields = "__all__"


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = "__all__"
