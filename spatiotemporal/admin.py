"""Django admin registration.

This module contains registration of the application's
automatic admin interface.

https://docs.djangoproject.com/en/4.0/ref/contrib/admin/
"""

from django.contrib import admin

from spatiotemporal.models import (
    Coverage,
    Measurement,
    SpatialThing,
    TimeUnit,
    Universe,
)

admin.site.register(TimeUnit)
admin.site.register(Universe)
admin.site.register(SpatialThing)
admin.site.register(Coverage)
admin.site.register(Measurement)
