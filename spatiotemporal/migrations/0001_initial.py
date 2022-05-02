import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
import django.contrib.postgres.indexes
import django.db.models.deletion
from django.db import migrations, models

import spatiotemporal.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("gis", "__first__"),
    ]

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
                ("name", models.CharField(blank=True, db_index=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                (
                    "links",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.URLField(), default=list, size=None
                    ),
                ),
                ("metadata", models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name="TimeUnit",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField(blank=True)),
                (
                    "links",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.URLField(), default=list, size=None
                    ),
                ),
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
                ("name", models.CharField(blank=True, db_index=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                (
                    "links",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.URLField(), default=list, size=None
                    ),
                ),
                ("properties", models.JSONField(default=dict)),
                (
                    "srid",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="gis.postgisspatialrefsys",
                    ),
                ),
                (
                    "timeunit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="spatiotemporal.timeunit",
                    ),
                ),
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
                (
                    "trajectory",
                    spatiotemporal.db.fields.TrajectoryField(
                        dim=4, editable=False, null=True, spatial_index=False, srid=0
                    ),
                ),
                ("name", models.CharField(blank=True, db_index=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                (
                    "links",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.URLField(), default=list, size=None
                    ),
                ),
                ("properties", models.JSONField(default=dict)),
                (
                    "universe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="spatiotemporal.universe",
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
                ("timestamp", models.IntegerField(db_index=True)),
                (
                    "geometry",
                    django.contrib.gis.db.models.fields.GeometryField(dim=3, srid=0),
                ),
                ("properties", models.JSONField()),
                (
                    "coverage",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="spatiotemporal.coverage",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Extent",
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
                ("timestamp", models.IntegerField()),
                (
                    "geometry",
                    django.contrib.gis.db.models.fields.GeometryField(dim=3, srid=0),
                ),
                ("metadata", models.JSONField(default=dict)),
                (
                    "thing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="spatiotemporal.spatialthing",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="coverage",
            name="universe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="spatiotemporal.universe",
            ),
        ),
        migrations.AddIndex(
            model_name="universe",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["properties"], name="spatiotempo_propert_85cae9_gin"
            ),
        ),
        migrations.AddIndex(
            model_name="spatialthing",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["trajectory"],
                name="spatiotemporal_trajectory_idx",
                opclasses=["GIST_GEOMETRY_OPS_ND"],
            ),
        ),
        migrations.AddIndex(
            model_name="spatialthing",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["properties"], name="spatiotempo_propert_87ea45_gin"
            ),
        ),
        migrations.AddIndex(
            model_name="measurement",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["properties"], name="spatiotempo_propert_b949eb_gin"
            ),
        ),
        migrations.AddConstraint(
            model_name="measurement",
            constraint=models.UniqueConstraint(
                fields=("coverage", "timestamp"), name="unique_coverage_timestamp"
            ),
        ),
        migrations.AddIndex(
            model_name="extent",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["metadata"], name="spatiotempo_metadat_822f27_gin"
            ),
        ),
        migrations.AddConstraint(
            model_name="extent",
            constraint=models.UniqueConstraint(
                fields=("thing", "timestamp"), name="unique_extent"
            ),
        ),
        migrations.AddIndex(
            model_name="coverage",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["metadata"], name="spatiotempo_metadat_dd6e2f_gin"
            ),
        ),
    ]
