"""Django models.

This module contains the application's Django models. The
vocabulary closely follows the W3C working group note:
"Spatial Data onthe Web Best Practices".

https://www.w3.org/TR/sdw-bp
"""


from django.contrib.gis.db.models import GeometryField, RasterField
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q


class Universe(models.Model):
    """A view of the world that includes everything of interest.

    Partitions the search space. A universe can be imaginary or real.
    It may define an epoch so that times expressed within it may be
    conceptually related across other universes, but this is not required.

    Examples:
        * earth
        * a photograph
        * the book "Lord of the Rings"

    https://en.wikipedia.org/wiki/Domain_of_discourse
    """

    epoch = models.DateTimeField(null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    links = ArrayField(models.URLField())
    properties = models.JSONField()


class SpatialThing(models.Model):
    """Abstraction of real world phenomena.

    Anything with spatial extent, (i.e. size, shape, or position)
    and is a combination of the real-world phenomenon and its
    abstraction.

    Examples are: people, places, or bowling balls.

    https://www.w3.org/TR/sdw-bp/#dfn-spatial-thing
    """

    universe = models.ForeignKey("Universe", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    links = ArrayField(models.URLField())
    properties = models.JSONField()


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
    properties = models.JSONField()


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

    trajectory = GeometryField(editable=False)
    metadata = models.JSONField()


class Measurement(models.Model):
    """A sample of a coverage.

    A coverage can consist of various "signals".

    For a vector geometry, the signal is the key in `properties`. The sample
    of that signal is a region in space (`geometry`) and time (`timestamp`) that
    relates the signal (`properties` key) to a value (`properties` value).

    For a raster geometry, the signal is the `attribute`. The sample of that
    signal is a region in space (`tile` projection) and time (`timestamp`) that
    relates the signal (`attribute`) to a value (`tile` value).

    The model differs between raster and vector data because the data structures
    fundamentally differ between them. However, we keep them in the same table
    because the information they carry is identical (see above). This allows
    us to later place constraints on this table. For example, we may decide in the
    future that a coverage must solely consist of either raster or vector measurements.
    Similarly, the signal will probably not be allowed to overlap within a measurement.
    """

    coverage = models.ForeignKey("Coverage", on_delete=models.CASCADE)
    timestamp = models.DurationField()
    # vector
    geometry = GeometryField(null=True)
    properties = models.JSONField(null=True)
    # raster
    tile = RasterField(null=True)
    attribute = models.CharField(max_length=255, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    Q(geometry__isnull=True)
                    | Q(tile__isnull=True)
                    & ~(Q(geometry__isnull=True) & Q(tile__isnull=True))
                ),
                name="measurement__vector_xor_raster_required",
            ),
            models.CheckConstraint(
                check=(
                    Q(attribute__isnull=True)
                    | Q(properties__isnull=True)
                    & ~(Q(attribute__isnull=True) & Q(properties__isnull=True))
                ),
                name="measurement__attribute_xor_properties_required",
            ),
            models.CheckConstraint(
                check=Q(tile__isnull=False) & Q(attribute__isnull=False),
                name="measurement__raster_attribute_required",
            ),
            models.CheckConstraint(
                check=Q(geometry__isnull=False) & Q(properties__isnull=False),
                name="measurement__vector_properties_required",
            ),
        ]
