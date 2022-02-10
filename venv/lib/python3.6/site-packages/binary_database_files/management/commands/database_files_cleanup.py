from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.db.models import FileField, ImageField
from django.apps import apps

from binary_database_files.models import File


class Command(BaseCommand):
    args = ""
    help = (
        "Deletes all files in the database that are not referenced by "
        "any model fields."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dryrun",
            action="store_true",
            dest="dryrun",
            default=False,
            help=(
                "If given, only displays the names of orphaned files "
                "and does not delete them."
            ),
        )
        parser.add_argument(
            "--filenames",
            default="",
            help="If given, only files with these names will be checked",
        )

    def handle(self, *args, **options):
        tmp_debug = settings.DEBUG
        settings.DEBUG = False
        names = set()
        dryrun = options["dryrun"]
        filenames = {_.strip() for _ in options["filenames"].split(",") if _.strip()}
        try:
            for model in apps.get_models():
                print("Checking model %s..." % (model,))
                for field in model._meta.fields:
                    if not isinstance(field, (FileField, ImageField)):
                        continue
                    # Ignore records with null or empty string values.
                    q = {"%s__isnull" % field.name: False}
                    xq = {field.name: ""}
                    subq = model.objects.filter(**q).exclude(**xq)
                    subq_total = subq.count()
                    subq_i = 0
                    for row in subq.iterator():
                        subq_i += 1
                        if subq_i == 1 or not subq_i % 100:
                            print("%i of %i" % (subq_i, subq_total))
                        f = getattr(row, field.name)
                        if f is None:
                            continue
                        if not f.name:
                            continue
                        names.add(f.name)

            # Find all database files with names not in our list.
            print("Finding orphaned files...")
            orphan_files = File.objects.exclude(name__in=names)
            if filenames:
                orphan_files = orphan_files.filter(name__in=filenames)
            orphan_files = orphan_files.only("name", "size")
            total_bytes = 0
            orphan_total = orphan_files.count()
            orphan_i = 0
            print("Deleting %i orphaned files..." % (orphan_total,))
            for f in orphan_files.iterator():
                orphan_i += 1
                if orphan_i == 1 or not orphan_i % 100:
                    print("%i of %i" % (orphan_i, orphan_total))
                total_bytes += f.size
                if dryrun:
                    print("File %s is orphaned." % (f.name,))
                else:
                    print("Deleting orphan file %s..." % (f.name,))
                    default_storage.delete(f.name)
            print("%i total bytes in orphan files." % total_bytes)
        finally:
            settings.DEBUG = tmp_debug
