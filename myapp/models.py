from django.db import models
from django.contrib.auth.models import User

class Measurement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    habit = models.CharField(max_length=100, blank=True, null=True)
    pant_size = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
