from typing import List, Tuple

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies: List[Tuple[str, str]] = []

    operations = [
        migrations.CreateModel(
            name="Coverage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "trajectory",
                    django.contrib.gis.db.models.fields.GeometryField(
                        editable=False, srid=4326
                    ),
                ),
                ("metadata", models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name="Universe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("epoch", models.DateTimeField(null=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "links",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.URLField(), size=None
                    ),
                ),
                ("properties", models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name="SpatialThing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "links",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.URLField(), size=None
                    ),
                ),
                ("properties", models.JSONField()),
                (
                    "universe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="image_annotations.universe",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Relationship",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("properties", models.JSONField()),
                (
                    "coverage",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="image_annotations.coverage",
                    ),
                ),
                (
                    "thing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="image_annotations.spatialthing",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Measurement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DurationField()),
                (
                    "geometry",
                    django.contrib.gis.db.models.fields.GeometryField(
                        null=True, srid=4326
                    ),
                ),
                ("properties", models.JSONField(null=True)),
                (
                    "tile",
                    django.contrib.gis.db.models.fields.RasterField(
                        null=True, srid=4326
                    ),
                ),
                ("attribute", models.CharField(max_length=255, null=True)),
                (
                    "coverage",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="image_annotations.coverage",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="measurement",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("geometry__isnull", True),
                    models.Q(
                        ("tile__isnull", True),
                        models.Q(
                            ("geometry__isnull", True),
                            ("tile__isnull", True),
                            _negated=True,
                        ),
                    ),
                    _connector="OR",
                ),
                name="vector_xor_raster_required",
            ),
        ),
        migrations.AddConstraint(
            model_name="measurement",
            constraint=models.CheckConstraint(
                check=models.Q(("tile__isnull", False), ("attribute__isnull", False)),
                name="raster_attribute_required",
            ),
        ),
        migrations.AddConstraint(
            model_name="measurement",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("geometry__isnull", False), ("properties__isnull", False)
                ),
                name="vector_properties_required",
            ),
        ),
    ]
