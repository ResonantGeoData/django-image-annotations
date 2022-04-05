"""Django admin registration.

This module contains registration of the application's
automatic admin interface.

https://docs.djangoproject.com/en/4.0/ref/contrib/admin/
"""

from django.contrib import admin

from spatiotemporal.models import (
    Coverage,
    Measurement,
    Relationship,
    SpatialThing,
    Universe,
)

admin.site.register(Universe)
admin.site.register(SpatialThing)
admin.site.register(Relationship)
admin.site.register(Coverage)
admin.site.register(Measurement)
