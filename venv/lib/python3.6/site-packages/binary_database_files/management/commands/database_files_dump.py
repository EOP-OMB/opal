from django.core.management.base import BaseCommand

from binary_database_files.models import File


class Command(BaseCommand):
    help = (
        "Dumps all files in the database referenced by FileFields "
        "or ImageFields onto the filesystem in the directory specified by "
        "MEDIA_ROOT."
    )

    def handle(self, *args, **options):
        File.dump_files(verbose=True)
