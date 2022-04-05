"""Django models.

This module contains the application's Django models. The
vocabulary closely follows the W3C working group note:
"Spatial Data on the Web Best Practices".

https://www.w3.org/TR/sdw-bp
"""


from django.contrib.gis.db.models import GeometryField
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.db.models import UniqueConstraint

from spatiotemporal.db.fields import TrajectoryField


class Universe(models.Model):
    """A view of the world that includes everything of interest.

    Partitions the search space. A universe can be imaginary or real.
    It may define an epoch so that times expressed within it may be
    conceptually related across other universes, but this is not required.

    Examples:
        * earth
        * a photograph
        * the setting of the book "Lord of the Rings"

    https://en.wikipedia.org/wiki/Domain_of_discourse
    """

    timeunit = models.CharField(max_length=200)
    epoch = models.DateTimeField(null=True)
    srid = models.ForeignKey(
        "gis.PostGISSpatialRefSys",
        on_delete=models.PROTECT,
        null=True,
    )
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    links = ArrayField(models.URLField(), default=list)
    properties = models.JSONField(default=dict)

    class Meta:
        indexes = [GinIndex(fields=["properties"])]


class SpatialThing(models.Model):
    """Abstraction of real world phenomena.

    Anything with spatial extent, (i.e. size, shape, or position)
    and is a combination of the real-world phenomenon and its
    abstraction.

    Examples are: people, places, or bowling balls.

    https://www.w3.org/TR/sdw-bp/#dfn-spatial-thing
    """

    universe = models.ForeignKey("Universe", on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    links = ArrayField(models.URLField(), default=list)
    properties = models.JSONField(default=dict)

    class Meta:
        indexes = [GinIndex(fields=["properties"])]


class Relationship(models.Model):
    """The relationships between a coverage and the thing it describes.

    Coverages may be spatially related to each other. This table allows
    spatial things to be spatially related to each other via their coverages.

    Example: an annotation (coverage) can describe the extent of a
    hot dog (spatial thing) within a photograph (universe) with a
    confidence (relationship property) of 98%.
    """

    thing = models.ForeignKey("SpatialThing", on_delete=models.CASCADE)
    coverage = models.ForeignKey("Coverage", on_delete=models.CASCADE)
    properties = models.JSONField(default=dict)

    class Meta:
        indexes = [GinIndex(fields=["properties"])]


class Coverage(models.Model):
    """A function that maps points in space and time to property values.

    For example, an aerial photograph can be thought of as a coverage that
    maps positions on the ground to colors. A river gauge maps points in time
    to flow values. A weather forecast maps points in space and time to
    values of temperature, wind speed, humidity and so forth.

    The `trajectory` is a materialized representation of the trajectory taken
    by the domain of the coverage.

    https://www.w3.org/TR/sdw-bp/#coverages
    """

    trajectory = TrajectoryField(
        editable=False,
        dim=4,
        srid=0,
        spatial_index=False,
        null=True,
    )
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    links = ArrayField(models.URLField(), default=list)
    metadata = models.JSONField(default=dict)

    class Meta:
        indexes = [
            GinIndex(fields=["metadata"]),
            GinIndex(
                fields=["trajectory"],
                name="spatiotemporal_trajectory_idx",
                opclasses=["GIST_GEOMETRY_OPS_ND"],
            ),
        ]


class Measurement(models.Model):
    """A sample of a coverage.

    A coverage can consist of various "signals". For a vector geometry, the
    signal is the key in `properties`. The sample of that signal is a region
    in space (`geometry`) and time (`timestamp`) that relates the signal
    (`properties` key) to a value (`properties` value).

    Later, a raster geometry may be added. For a raster geometry, a potential
    signal is the `n`th element of the `attributes` array. The sample of that
    signal is a region in space (`tile` projection) and time (`timestamp`) that
    relates the signal (`attributes` index `n`) to a value (`tile` value) in a
    band (`tile` band `n`).

    A measurement without signals should be interpreted as an extent. A raster
    extent measurment would be a 1-bit raster dataset where ON covers the
    footprint of the extent.

    The model differs between raster and vector data because the data
    structures fundamentally differ between them. However, we would keep them
    in the same table because the information they carry is identical (see
    above). This allows us to place constraints on this table. For example, we
    may require that a coverage must solely consist of either tile or geometry
    measurements. Similarly, the signal would not be allowed to overlap within
    a coverage.
    """

    coverage = models.ForeignKey("Coverage", on_delete=models.CASCADE)
    timestamp = models.IntegerField(db_index=True)
    geometry = GeometryField(dim=3, srid=0)
    properties = models.JSONField(null=True)

    class Meta:
        indexes = [GinIndex(fields=["properties"])]
        constraints = [
            UniqueConstraint(
                fields=["coverage", "timestamp"],
                name="unique_coverage_timestamp",
            )
        ]
