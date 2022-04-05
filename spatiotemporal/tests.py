import datetime

from django.test import TestCase

from .models import Coverage, Measurement, Relationship, SpatialThing, Universe


class Constraints(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.universe = Universe.objects.create(
            epoch=datetime.datetime(2001, 4, 12),
            srid=None,
            name="Jovian system: cube 12-156A",
            description="A cubic sector of space near Jupiter's moon Io with time beginning at first observation of Tycho Magnetic Anomaly-2",
            links=["https://en.wikipedia.org/wiki/Io_(moon)"],
            properties={},
        )
        cls.spatialthing = SpatialThing.objects.create(
            universe=cls.universe,
            name="Tycho Magnetic Anomaly-2",
            description="A larger variant of the first observed alien Monolith. Same proportions. Found suddenly in the Jovian system.",
            links=["https://en.wikipedia.org/wiki/Monolith_(Space_Odyssey)"],
            properties={"code": "TMA-2", "generation": 2, "magnetic": False},
        )

    def test_1(self):
        # Some test using self.foo
        ...

    def test_2(self):
        # Some other test using self.foo
        ...
