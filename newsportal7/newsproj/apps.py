from django.apps import AppConfig
import redis


class NewsprojConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsproj'

    def ready(self):
        import newsproj.signals

red = redis.Redis(
    host='redis-13612.c89.us-east-1-3.ec2.cloud.redislabs.com',
    port=13612,
    password='akV6JTyll0tn6Q1hWim1GoPsBudMCN4N'
)