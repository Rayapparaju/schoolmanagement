from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_default_admin(sender, **kwargs):
    from django.contrib.auth.models import User
    from schoolapp.models import Notice
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser('admin', 'admin@school.com', 'admin123')
    if Notice.objects.count() == 0:
        Notice.objects.create(
            title='Welcome to SchoolMS',
            content='School Management System is up and running. Use admin/admin123 to login.',
        )


class SchoolappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'schoolapp'

    def ready(self):
        post_migrate.connect(create_default_admin, sender=self)
