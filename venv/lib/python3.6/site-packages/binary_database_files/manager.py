from django.db import models


class FileManager(models.Manager):
    def get_from_name(self, name):
        return self.get(name=name)
