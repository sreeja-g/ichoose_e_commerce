from djongo import models
from django import forms

class ListFormField(forms.CharField):
    def to_python(self, value):
        if value is None:
            value = ""
        return value.split(",")

    def prepare_value(self, value):
        if value is None:
            value = []
        return ",".join(value)


class CustomListField(models.ListField):
    def formfield(self, **kwargs):
        return ListFormField(max_length=1000)


class user_details(models.Model):
    user_id=models.IntegerField(null=False)
    user_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=50)
    class Meta:
        abstract = True


class user_details_form(forms.ModelForm):
    class Meta:
        model = user_details
        fields = (
            'user_id', 'user_name','email',
            'phone_number'
        )


class orders_sellers(models.Model):
    order_id = models.IntegerField(default=None)
    buyer_details = models.EmbeddedField(model_container=user_details,model_form_class=user_details_form)
    date_of_order = models.DateTimeField()
    told_date_of_order = models.DateTimeField()
    date_of_delivery = models.DateTimeField()
    order_details = CustomListField(default=[])
    quantity = models.IntegerField(null=False)
    payment_status = models.BooleanField(default=False)
    delivery_status = models.BooleanField(default=False)
    class Meta:
        abstract = True

class orders_sellers_form(forms.ModelForm):
    class Meta:
        model = orders_sellers
        fields = (
            'order_id','buyer_details', 'date_of_order',
            'told_date_of_order','date_of_delivery','order_details','quantity','payment_status',
            'delivery_status'
        )


class product(models.Model):
    seller_details = models.EmbeddedField(model_container=user_details,model_form_class=user_details_form)
    product_title = models.TextField()
    category_1 = models.TextField()
    category_2 = models.TextField()
    product_description = models.TextField()

    images = CustomListField(default=[])
    product_quantity_available= CustomListField(default=[])
    additional_information=models.TextField()

    product_customisation_available= CustomListField(default=[])
    additional_customization_information=models.TextField()

    orders=models.ArrayField(model_container=orders_sellers,model_form_class=orders_sellers_form,default=[])
    #ratings_comments=models.ArrayField(model_container=rating_comments_products,default=[])
    date_of_post=models.DateTimeField()

    objects = models.DjongoManager()


class product_form(forms.ModelForm):
    class Meta:
        model = product
        fields = (
            'seller_details', 'product_title',
            'category_1','category_2','product_description','images','product_quantity_available',
            'additional_information','product_customisation_available','additional_customization_information',
            'orders', 'date_of_post'
        )


class sellers(models.Model):
    seller_details = models.EmbeddedField(model_container=user_details,model_form_class=user_details_form)
    #posted_products=models.ArrayField(model_container=product,model_form_class=product_form,default=[])
    product_orders=models.ArrayField(model_container=orders_sellers,model_form_class=orders_sellers_form,default=[])
    #loans_applied=models.ArrayField(model_container=loan_details,default=[])
    #loans_accepted=models.ArrayField(model_container=loan_details,default=[])
    #customization_requests = models.ArrayField(model_container=customization_request_sellers, default=[])

    objects = models.DjongoManager()

class sellers_form(forms.ModelForm):
    class Meta:
        model = sellers
        fields = (
            'seller_details',
            'product_orders'
        )

#---------------------------------------------------------------------------------------------------------------