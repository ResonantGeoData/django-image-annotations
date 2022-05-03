import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "imageannotationsd.settings")
django.setup()

import orjson
from django.contrib.gis.geos import LineString

from spatiotemporal.models import (
    Coverage,
    Measurement,
    Relationship,
    SpatialThing,
    Universe,
)

universe = Universe.objects.get_or_create(
    name="Image 5e6a76bc4203de4bdeffcbc6",
    defaults={
        "timeunit": "seconds",
        "epoch": None,
        "srid": None,
        "description": "",
        "links": ["http://parakon:8088/api/v1/image/5e6a76bc4203de4bdeffcbc6"],
        "properties": {},
    },
)[0]
thing = SpatialThing.objects.get_or_create(
    name="Whole Slide Boundary",
    defaults={
        "description": "",
        "links": ["http://parakon:8088/api/v1/annotation/5e6a76bc4203de4bdeffcbc6"],
    },
)[0]

Measurement.objects.exclude(pk__in=(1, 2)).delete()
Relationship.objects.exclude(pk=1).delete()
Coverage.objects.exclude(pk=1).delete()


with open(".scratch/sample.json", "rb") as f:
    data = orjson.loads(f.read())


def gen_coverage():
    for elm in data["annotation"]["elements"]:
        yield Coverage(
            name=f"Element {elm['id']}",
            universe=universe,
            description="",
            links=[],
            metadata={
                "fillColor": elm["fillColor"],
                "lineColor": elm["lineColor"],
            },
        )


coverages = Coverage.objects.bulk_create(gen_coverage(), batch_size=10000)


def gen_relationships():
    for cov in coverages:
        yield Relationship(
            thing=thing,
            coverage=cov,
        )


Relationship.objects.bulk_create(gen_relationships(), batch_size=10000)


def gen_measurements():
    for cov, elm in zip(coverages, data["annotation"]["elements"]):
        yield Measurement(
            coverage=cov,
            timestamp=0,
            geometry=LineString(elm["points"]),
            properties=None,
        )


Measurement.objects.bulk_create(gen_measurements(), batch_size=10000)
