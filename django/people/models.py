from django.db import models
from django.contrib.auth.models import User as U


# Create your models here.
class User(models.Model):
    user = models.OneToOneField(U,
                                on_delete=models.CASCADE,
                                primary_key=True)
