"""Django application registration.

This module contains the application's Django registration.
It is mainly used to hook into the application's "ready"
state.


https://docs.djangoproject.com/en/4.0/ref/applications/
"""


from django.apps import AppConfig
from django.db.models.signals import post_delete, post_save


class SpatioTemporalConfig(AppConfig):

    default_auto_field = "django.db.models.BigAutoField"
    name = "spatiotemporal"

    def ready(self):
        from spatiotemporal import signals

        post_save.connect(signals.update_trajectory)
        post_delete.connect(signals.update_trajectory)
