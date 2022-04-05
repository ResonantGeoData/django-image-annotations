from django.contrib.gis.db.models import GeometryField
from django.db.models import Field


class BitField(Field):
    """A bit string field of length 1."""

    def db_type(self, connection):
        return "BIT"


class TrajectoryField(GeometryField):
    """A geometry field for making the 4D trajectory.

    Will not accept read/write.
    """

    geom_type = "LINESTRINGZM"
    geom_class = None
    form_class = None
    description = None
