"""Django signals.

This module contains the application's callback functions
for handling signals.

https://docs.djangoproject.com/en/4.0/topics/signals/
"""
from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import F

from .db.functions import Box3D, MakeLine, MakePoint, XMax, XMin, YMax, YMin, ZMax, ZMin
from .models import Coverage, Measurement


def update_trajectory(sender, instance: Measurement, **kwargs):
    """Update `Coverage.trajectory` when `Measurement` is changed."""
    if sender is Measurement:
        Coverage.objects.filter(pk=instance.coverage_id).update(
            trajectory=MakeLine(
                ArraySubquery(
                    (
                        Measurement.objects.filter(coverage_id=instance.coverage_id)
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
