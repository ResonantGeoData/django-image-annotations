"""Django database functions.

This module supplements Django's own coverage of Postgres
and PostGIS functions.

https://docs.djangoproject.com/en/4.0/ref/models/expressions/#func-expressions-1
"""


from django.contrib.gis.db.models import GeometryField, LineStringField, PointField
from django.db.models import FloatField, Func


class Box3D(Func):
    """Compute the 3D bounding box of a geometry."""

    function = "Box3D"
    output_field = GeometryField()


class XMax(Func):
    """Returns the X maxima of a 2D or 3D bounding box or a geometry."""

    function = "ST_XMax"
    output_field: "FloatField[float, float]" = FloatField()


class XMin(Func):
    """Returns the X minima of a 2D or 3D bounding box or a geometry."""

    function = "ST_XMin"
    output_field: "FloatField[float, float]" = FloatField()


class YMax(Func):
    """Returns the Y maxima of a 2D or 3D bounding box or a geometry."""

    function = "ST_YMax"
    output_field: "FloatField[float, float]" = FloatField()


class YMin(Func):
    """Returns the Y minima of a 2D or 3D bounding box or a geometry."""

    function = "ST_YMin"
    output_field: "FloatField[float, float]" = FloatField()


class ZMax(Func):
    """Returns the Z maxima of a 2D or 3D bounding box or a geometry."""

    function = "ST_ZMax"
    output_field: "FloatField[float, float]" = FloatField()


class ZMin(Func):
    """Returns the Z minima of a 2D or 3D bounding box or a geometry."""

    function = "ST_ZMin"
    output_field: "FloatField[float, float]" = FloatField()


class MakePoint(Func):
    """Compute the pixel type of the first band of a raster."""

    function = "ST_MakePoint"
    output_field = PointField(srid=0)


class MakeLine(Func):
    """Compute the pixel type of the first band of a raster."""

    function = "ST_MakeLine"
    output_field = LineStringField(srid=0)
