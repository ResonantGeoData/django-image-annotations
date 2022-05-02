"""Django application registration.

This module contains the application's Django registration.
It is mainly used to hook into the application's "ready"
state.


https://docs.djangoproject.com/en/4.0/ref/applications/
"""


from django.apps import AppConfig


class PannotationsConfig(AppConfig):

    default_auto_field = "django.db.models.BigAutoField"
    name = "pannotations"
