from djongo import models
from ichoose.models import user_details


class seller_verification_process(models.Model):

    seller_details = models.EmbeddedField(model_container=user_details)
    name= models.CharField(max_length=100)
    phone_number=models.CharField(max_length=50)

    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=50)

    purpose = models.TextField()

    images = models.ListField(default=[])
    files = models.ListField(default=[])

    Verification_step_1 = models.BooleanField(default=False)
    Verification_step_2 = models.BooleanField(default=False)
    Verification_step_3 = models.BooleanField(default=False)