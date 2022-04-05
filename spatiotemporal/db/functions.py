from django.contrib.gis.db.models import GeometryField, LineStringField, PointField
from django.db.models import CharField, FloatField, Func, IntegerField


class NumBands(Func):
    """Compute the number of bands in a PostGIS raster."""

    function = "ST_NumBands"
    output_field: "IntegerField[int, int]" = IntegerField()


class PixelType(Func):
    """Compute the pixel type of the first band of a raster."""

    function = "ST_BandPixelType"
    output_field: "CharField[str, str]" = CharField()


class Box3D(Func):
    """Compute the 3D bounding box of a geometry."""

    function = "Box3D"
    output_field = GeometryField()


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

    function = "ST_MakeLine"
    output_field = PointField()


class MakeLine(Func):
    """Compute the pixel type of the first band of a raster."""

    function = "ST_MakeLine"
    output_field = LineStringField()
