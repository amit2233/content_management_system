from django.db import models

# Create your models here.
from multiselectfield import MultiSelectField

from authentication.models import User


class Content(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    body = models.CharField(max_length=300)
    summary = models.CharField(max_length=60)
    document = models.FileField()
    category = MultiSelectField(null=True)
