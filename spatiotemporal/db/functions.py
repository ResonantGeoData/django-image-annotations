from django.contrib.gis.db.models import LineStringField, PointField
from django.db.models import FloatField, Func


class XMax(Func):
    """Returns the X maxima of a 2D or 3D bounding box or a geometry."""

    function = "ST_XMax"
    output_field = FloatField()


class XMin(Func):
    """Returns the X minima of a 2D or 3D bounding box or a geometry."""

    function = "ST_XMin"
    output_field = FloatField()


class YMax(Func):
    """Returns the Y maxima of a 2D or 3D bounding box or a geometry."""

    function = "ST_YMax"
    output_field = FloatField()


class YMin(Func):
    """Returns the Y minima of a 2D or 3D bounding box or a geometry."""

    function = "ST_YMin"
    output_field = FloatField()


class ZMax(Func):
    """Returns the Z maxima of a 2D or 3D bounding box or a geometry."""

    function = "ST_ZMax"
    output_field = FloatField()


class ZMin(Func):
    """Returns the Z minima of a 2D or 3D bounding box or a geometry."""

    function = "ST_ZMin"
    output_field = FloatField()


class MakePoint(Func):
    """Compute the pixel type of the first band of a raster."""

    function = "ST_MakePoint"
    output_field = PointField(srid=0)


class MakeLine(Func):
    """Compute the pixel type of the first band of a raster."""

    function = "ST_MakeLine"
    output_field = LineStringField(srid=0)
