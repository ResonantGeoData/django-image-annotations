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


class TimeUnit(models.Model):
    """Time unit lookup table."""

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    links = ArrayField(models.URLField(), default=list)


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

    timeunit = models.ForeignKey("TimeUnit", on_delete=models.PROTECT)
    epoch = models.DateTimeField(null=True)
    srid = models.ForeignKey(
        "gis.PostGISSpatialRefSys",
        on_delete=models.PROTECT,
        null=True,
    )
    name = models.CharField(max_length=255, blank=True, db_index=True)
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

    The `trajectory` is a materialized representation of the
    spatiotemporal extent of the spatial thing.

    https://www.w3.org/TR/sdw-bp/#dfn-spatial-thing
    """

    trajectory = TrajectoryField(
        editable=False,
        dim=4,
        srid=0,
        spatial_index=False,
        null=True,
    )
    universe = models.ForeignKey("Universe", on_delete=models.CASCADE)
    name = models.CharField(blank=True, db_index=True, max_length=255)
    description = models.TextField(blank=True)
    links = ArrayField(models.URLField(), default=list)
    properties = models.JSONField(default=dict)

    class Meta:
        indexes = [
            GinIndex(
                fields=["trajectory"],
                name="spatiotemporal_trajectory_idx",
                opclasses=["GIST_GEOMETRY_OPS_ND"],
            ),
            GinIndex(fields=["properties"]),
        ]


class Extent(models.Model):
    """A spatial extent.

    Describes the spatial extent of a spatial thing. This is really
    just a dimensionless coverage, but it is useful to represent
    it as a seperate model. Otherwise, the special meaning of `NULL`
    for `properties` in `Coverage`/`Measurement` would be confusing.
    """

    thing = models.ForeignKey("SpatialThing", on_delete=models.CASCADE)
    timestamp = models.IntegerField()
    geometry = GeometryField(dim=3, srid=0)
    metadata = models.JSONField(default=dict)

    class Meta:
        constraints = [
            UniqueConstraint(
                name="unique_extent",
                fields=["thing", "timestamp"],
            )
        ]
        indexes = [GinIndex(fields=["metadata"])]


class Coverage(models.Model):
    """A function that maps points in space and time to property values.

    For example, an aerial photograph can be thought of as a coverage that
    maps positions on the ground to colors. A river gauge maps points in time
    to flow values. A weather forecast maps points in space and time to
    values of temperature, wind speed, humidity and so forth.

    https://www.w3.org/TR/sdw-bp/#coverages
    """

    universe = models.ForeignKey("Universe", on_delete=models.CASCADE)
    name = models.CharField(blank=True, db_index=True, max_length=255)
    description = models.TextField(blank=True)
    links = ArrayField(models.URLField(), default=list)
    metadata = models.JSONField(default=dict)

    class Meta:
        indexes = [GinIndex(fields=["metadata"])]


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
    properties = models.JSONField()

    class Meta:
        indexes = [GinIndex(fields=["properties"])]
        constraints = [
            UniqueConstraint(
                fields=["coverage", "timestamp"],
                name="unique_coverage_timestamp",
            )
        ]
