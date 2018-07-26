from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'order'

    def ready(self):
        import order.signals.signals
