from djongo import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile = models.CharField(max_length=16)
    address = models.TextField()
    bank_details=models.TextField()

    email = models.EmailField(max_length=254, unique=True)
    def __str__(self):

        return self.username
