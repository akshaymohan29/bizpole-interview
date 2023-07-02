from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Activity(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_fetched = models.DateTimeField(null=True, blank=True)
    # Add any other fields you need for an activity

    def __str__(self):
        return self.name
