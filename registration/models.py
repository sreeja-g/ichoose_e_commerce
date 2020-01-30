from djongo import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile = models.CharField(max_length=16)
    address = models.TextField()
    bank_details=models.TextField()

    def __str__(self): 

        return self.username

