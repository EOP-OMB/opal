from django.conf import settings
from django.core.management.base import BaseCommand

from binary_database_files.models import File


class Command(BaseCommand):
    args = "<filename 1> <filename 2> ... <filename N>"
    help = (
        "Regenerates hashes for files. If no filenames given, " + "rehashes everything."
    )

    def handle(self, *args, **options):
        tmp_debug = settings.DEBUG
        settings.DEBUG = False
        try:
            q = File.objects.all()
            if args:
                q = q.filter(name__in=args)
            total = q.count()
            i = 1
            for f in q.iterator():
                print("%i of %i: %s" % (i, total, f.name))
                f._content_hash = None
                f.save()
                i += 1
        finally:
            settings.DEBUG = tmp_debug
