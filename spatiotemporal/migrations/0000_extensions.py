from django.contrib.postgres.operations import BtreeGistExtension
from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("gis", "__first__"),
    ]

    operations = [BtreeGistExtension()]
