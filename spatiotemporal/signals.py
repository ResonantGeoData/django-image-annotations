"""Django signals.

This module contains the application's callback functions
for handling signals.

https://docs.djangoproject.com/en/4.0/topics/signals/
"""
from django.contrib.postgres.expressions import ArraySubquery  # type: ignore
from django.db.models import F

from spatiotemporal.db.functions import (
    Box3D,
    MakeLine,
    MakePoint,
    XMax,
    XMin,
    YMax,
    YMin,
    ZMax,
    ZMin,
)
from spatiotemporal.models import Extent, SpatialThing


def update_trajectory(sender, instance: Extent, **kwargs):
    """Update `SpatialThing.trajectory` when `Extent` is changed."""
    if sender is Extent:
        SpatialThing.objects.filter(pk=instance.thing_id).update(
            trajectory=MakeLine(
                ArraySubquery(
                    (
                        Extent.objects.filter(thing_id=instance.thing_id)
                        .order_by("timestamp")
                        .annotate(
                            bbox=Box3D("geometry"),
                            point=MakePoint(
                                (XMin("bbox") + XMax("bbox")) / 2,
                                (YMin("bbox") + YMax("bbox")) / 2,
                                (ZMin("bbox") + ZMax("bbox")) / 2,
                                F("timestamp"),
                            ),
                        )
                        .values("point")
                    )
                )
            )
        )
