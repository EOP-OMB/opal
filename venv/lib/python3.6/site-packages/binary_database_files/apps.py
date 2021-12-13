from django.apps import AppConfig


class DatabaseFilesAppConfig(AppConfig):
    """AppConfig to make binary_database_files compatible with app loading"""

    name = "binary_database_files"
    label = "binary_database_files"
    verbose_name = "django-binary-database-files"
