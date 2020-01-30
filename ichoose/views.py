from django.shortcuts import HttpResponse
from .models import *
from datetime import datetime
i=0
def new(request):
    p=product(seller_details=user_details(user_id=1,user_name="sreeja",email="a@g.com",phone_number="12345"),product_title="title",category_1="category_1",category_2="category_2",product_description="product_description",product_quantity_available=[{"red,5":(2,100,50),"blue,5":(2,100,50)}],product_customisation_available=[{"colors":["red","blue"],"sizes":[5,9,7,6]}],orders=[],ratings_comments=[],date_of_post=datetime.now())
    p.orders.append(orders_products(buyer_details=user_details(user_id=1,user_name="sreeja",email="a@g.com",phone_number="12345"),date_of_order=datetime.now(),delivery_status=False,payment_status=False))
    p.save()
    x=product.objects.all()
    return HttpResponse(x)
