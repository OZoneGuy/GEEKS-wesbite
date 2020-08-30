from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=100)
    short_desc = models.CharField(max_length=500)
    long_desc = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    banner = models.FileField(upload_to="events/%Y/%m")
