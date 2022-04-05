"""Django database fields.

This module supplements Django's own coverage of Postgres
and PostGIS types.

https://docs.djangoproject.com/en/4.0/howto/custom-model-fields/
"""

from django.contrib.gis.db.models import GeometryField


class TrajectoryField(GeometryField):
    """A geometry field for making the 4D trajectory.

    Will not accept read/write.
    """

    geom_type = "LINESTRINGZM"
    geom_class = None
    form_class = None
    description = None
