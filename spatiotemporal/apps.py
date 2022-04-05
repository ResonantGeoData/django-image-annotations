from django.apps import AppConfig
from django.db.models.signals import post_delete, post_save


class SpatioTemporalConfig(AppConfig):

    default_auto_field = "django.db.models.BigAutoField"
    name = "spatiotemporal"

    def ready(self):
        from spatiotemporal import signals

        post_save.connect(signals.update_trajectory)
        post_delete.connect(signals.update_trajectory)
