from django.conf import settings
from django.db import models
from django.utils import timezone

from django.db.models import BinaryField

from binary_database_files import utils
from binary_database_files.utils import write_file, is_fresh
from binary_database_files.manager import FileManager


class File(models.Model):

    objects = FileManager()

    name = models.CharField(
        max_length=255, unique=True, blank=False, null=False, db_index=True
    )

    size = models.PositiveIntegerField(db_index=True, blank=False, null=False)

    content = BinaryField(blank=False, null=False)

    created_datetime = models.DateTimeField(
        db_index=True, default=timezone.now, verbose_name="Created datetime"
    )

    _content_hash = models.CharField(
        db_column="content_hash", db_index=True, max_length=128, blank=True, null=True
    )

    class Meta:
        db_table = "binary_database_files_file"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        # Check for and clear old content hash.
        if self.id:
            old = File.objects.get(id=self.id)
            if old.content != self.content:
                self._content_hash = None

        # Recalculate new content hash.
        self.content_hash

        return super(File, self).save(*args, **kwargs)

    @property
    def content_hash(self):
        if not self._content_hash and self.content:
            self._content_hash = utils.get_text_hash(self.content)
        return self._content_hash

    def dump(self, check_hash=False):
        """
        Writes the file content to the filesystem.

        If check_hash is true, clears the stored file hash and recalculates.
        """
        if is_fresh(self.name, self._content_hash):
            return
        write_file(self.name, self.content, overwrite=True)
        if check_hash:
            self._content_hash = None
        self.save()

    @classmethod
    def dump_files(cls, debug=True, verbose=False):
        """
        Writes all files to the filesystem.
        """
        if debug:
            tmp_debug = settings.DEBUG
            settings.DEBUG = False
        try:
            q = cls.objects.only("id", "name", "_content_hash").values_list(
                "id", "name", "_content_hash"
            )
            total = q.count()
            if verbose:
                print("Checking %i total files..." % (total,))
            i = 0
            for (file_id, name, content_hash) in q.iterator():
                i += 1
                if verbose and not i % 100:
                    print("%i of %i" % (i, total))
                if not is_fresh(name=name, content_hash=content_hash):
                    if verbose:
                        print(
                            ("File %i-%s is stale. Writing to local file " "system...")
                            % (file_id, name)
                        )
                    f = File.objects.get(id=file_id)
                    write_file(f.name, f.content, overwrite=True)
                    f._content_hash = None
                    f.save()
        finally:
            if debug:
                settings.DEBUG = tmp_debug
