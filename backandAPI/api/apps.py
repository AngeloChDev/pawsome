from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    class Meta:
        app_label="api"
    
    def ready(self) -> None:
        self.import_models()
        return print('models')