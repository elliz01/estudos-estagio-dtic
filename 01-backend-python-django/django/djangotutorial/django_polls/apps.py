from django.apps import AppConfig


class PollsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutofield"
    name = "django_polls"
    label = "polls"


