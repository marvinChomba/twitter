from django.apps import AppConfig

app_name = "auth"

class AuthenticationConfig(AppConfig):
    name = 'authentication'

    def ready(self):
        import authentication.signals
