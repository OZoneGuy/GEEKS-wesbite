from django.db import models


class Event(models.Model):
    title = models.CharField()
    short_desc = models.CharField()
    long_desc = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    banner = models.FileField(upload_to="events/%Y/%m")
