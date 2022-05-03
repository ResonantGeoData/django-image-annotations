from typing import Any, Generic, Type, TypeVar

from pydantic import BaseModel

from spatiotemporal.models import SpatialThing

T = TypeVar("T", bound=BaseModel)

REGISTRY: dict[str, "PannotationFormat"] = {}


class PannotationFormat(Generic[T]):
    name: str
    model: Type[T]

    def __init_subclass__(cls, **kwargs) -> None:
        if cls.name in REGISTRY:
            raise ValueError(f"{cls.name} already registered to {REGISTRY[cls.name]}")
        REGISTRY[cls.name] = cls()

    def render(self, thing: SpatialThing) -> T:
        ...


class GeoJSON(PannotationFormat):
    name = "geojson"
    model = dict

    def render(self, thing: SpatialThing) -> dict[str, Any]:
        return {
            "type": "Feature",
            "geometry": {"type": "Point"},
            "properties": {
                "name": thing.name,
                "description": thing.description,
            },
        }
