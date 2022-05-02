"""Django URL configuration.

The `urlpatterns` list routes URLs to views. This is for the
`spatiotemporal` application.

https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""


from django.urls import include, path
from rest_framework.routers import SimpleRouter

from spatiotemporal.views import (
    CoverageViewSet,
    MeasurementViewSet,
    RelationshipViewSet,
    SpatialThingViewSet,
    TimeUnitViewSet,
    UniverseViewSet,
)

router = SimpleRouter()
router.register(r"timeunits", TimeUnitViewSet)
router.register(r"universes", UniverseViewSet)
router.register(r"spatialthings", SpatialThingViewSet)
router.register(r"relationships", RelationshipViewSet)
router.register(r"coverages", CoverageViewSet)
router.register(r"measurements", MeasurementViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
