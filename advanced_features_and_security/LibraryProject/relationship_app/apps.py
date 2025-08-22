from django.apps import AppConfig
from django import forms



class RelationshipAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relationship_app'

def ready(self):
        # import signals so they get registered
        import relationship_app.signals
