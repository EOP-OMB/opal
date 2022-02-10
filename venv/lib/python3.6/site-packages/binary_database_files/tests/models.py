from django.db import models


class Thing(models.Model):
    upload = models.FileField(upload_to="i/special", max_length=500)
