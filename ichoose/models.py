from djongo import models
from registration.models import User


#---------------------------------ABSTRACT MODELS---------------------------------------------------

class user_details(models.Model):
    user_id=models.IntegerField(null=False)
    user_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=50)
    class Meta:
        abstract = True

class orders_products(models.Model):
    buyer_details = models.EmbeddedField(model_container=user_details)
    date_of_order=models.DateTimeField()
    payment_status=models.BooleanField(default=False)
    delivery_status=models.BooleanField(default=False)
    class Meta:
        abstract = True

class rating_comments_products(models.Model):
    buyer_details = models.EmbeddedField(model_container=user_details)
    date_of_rating_comments=models.DateTimeField()
    rating=models.TextField()
    comment=models.TextField()
    class Meta:
        abstract = True

#-------------------------------------------------------------------------------------------------------

class product(models.Model):
    seller_details = models.EmbeddedField(model_container=user_details)
    product_title = models.TextField()
    category_1 = models.TextField()
    category_2 = models.TextField()
    product_description = models.TextField()
    product_quantity_available=models.ListField(default=[])
    product_customisation_available=models.ListField(default=[])
    orders=models.ArrayField(model_container=orders_products,default=[])
    ratings_comments=models.ArrayField(model_container=rating_comments_products,default=[])
    date_of_post=models.DateTimeField()


#---------------------------------ABSTRACT MODELS---------------------------------------------------

class orders_buyers(models.Model):
    product_details = models.EmbeddedField(model_container=product)
    date_of_order=models.DateTimeField()
    payment_status=models.BooleanField(default=False)
    delivery_status=models.BooleanField(default=False)
    class Meta:
        abstract = True


class rating_comments_buyers(models.Model):
    product_details = models.EmbeddedField(model_container=product)
    date_of_rating_comments=models.DateTimeField()
    rating = models.TextField()
    comment = models.TextField()
    class Meta:
        abstract = True


class customization_request_buyers(models.Model):
    product_details = models.EmbeddedField(model_container=product)
    request_description=models.TextField()
    date_of_request = models.DateTimeField()
    status = models.BooleanField(default=False)
    class Meta:
        abstract = True

#-----------------------------------------------------------------------------------------------

class buyers(models.Model):
    buyer_details = models.EmbeddedField(model_container=user_details)
    wishlist = models.ListField(default=[])
    add_to_cart = models.ListField(default=[])
    orders= models.ArrayField(model_container=orders_buyers,default=[])
    customization_requests=models.ArrayField(model_container=customization_request_buyers,default=[])
    ratings_comments=models.ArrayField(model_container=rating_comments_buyers,default=[])


#---------------------------------ABSTRACT MODELS---------------------------------------------------

class customization_request_sellers(models.Model):
    buyer_details = models.EmbeddedField(model_container=user_details)
    product_details = models.EmbeddedField(model_container=product)
    request_description=models.TextField()
    date_of_request = models.DateTimeField()
    status = models.BooleanField(default=False)
    class Meta:
        abstract = True

#---------------------------------------------------------------------------------------------------

class loan_details(models.Model):
    loner_details=models.EmbeddedField(model_container=user_details)
    loan_amount=models.IntegerField()
    intrest_amount=models.IntegerField()
    requirements=models.TextField()
    terms_and_conditions=models.TextField()

#---------------------------------ABSTRACT MODELS---------------------------------------------------

class loan_request_seller(models.Model):
    loan=models.EmbeddedField(model_container=loan_details)
    request_description=models.TextField()
    date_of_request=models.DateTimeField()
    status=models.BooleanField(default=False)
    contact_info_sent=models.TextField(default="")
    class Meta:
        abstract = True

class orders_sellers(models.Model):
    buyer_details = models.EmbeddedField(model_container=user_details)
    product_details = models.EmbeddedField(model_container=product)
    date_of_order=models.DateTimeField()
    payment_status=models.BooleanField(default=False)
    delivery_status=models.BooleanField(default=False)
    class Meta:
        abstract = True


#----------------------------------------------------------------------------------------------

class sellers(models.Model):
    seller_details = models.EmbeddedField(model_container=user_details)
    posted_products=models.ArrayField(model_container=product,default=[])
    product_orders=models.ArrayField(model_container=orders_sellers,default=[])
    loans_applied=models.ArrayField(model_container=loan_details,default=[])
    loans_accepted=models.ArrayField(model_container=loan_details,default=[])
    verification_status=models.BooleanField(default=False)
    verification_data=models.FileField()
    customization_requests = models.ArrayField(model_container=customization_request_sellers, default=[])


#---------------------------------ABSTRACT MODELS---------------------------------------------------

class loan_request_loaner(models.Model):
    loan=models.EmbeddedField(model_container=loan_details)
    seller_details = models.EmbeddedField(model_container=user_details)
    request_description=models.TextField()
    date_of_request=models.DateTimeField()
    status=models.BooleanField(default=False)
    contact_info_sent=models.TextField(default="")
    class Meta:
        abstract = True

#------------------------------------------------------------------------------------------------------

class loaners(models.Model):
    loaner_details = models.EmbeddedField(model_container=user_details)
    posted_loans=models.ArrayField(model_container=loan_details,default=[])
    loans_accepted=models.ArrayField(model_container=loan_details,default=[])


