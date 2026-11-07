from django.apps import AppConfig
from django.db.backends.signals import connection_created


class HotelConfig(AppConfig):
    name = 'hotel'

    
    def ready(self):
        connection_created.connect(self.extend_sqlite)

    @staticmethod
    def extend_sqlite(sender, connection, **kwargs):
        if connection.vendor == 'sqlite':
            connection.connection.create_function(
                'LOWER',
                1,
                lambda x: x.casefold() if x else x
            )