from django.shortcuts import HttpResponse
from .models import *
import datetime
from ichoose.models import sellers_form,orders_sellers_form,ListFormField

i=0
def new(request):
    p=product(seller_details=user_details(user_id=1,user_name="sreeja",email="a@g.com",phone_number="12345"),product_title="title",category_1="category_1",category_2="category_2",product_description="product_description",product_quantity_available=[{"red,5":(2,100,50),"blue,5":(2,100,50)}],product_customisation_available=[{"colors":["red","blue"],"sizes":[5,9,7,6]}],orders=[],ratings_comments=[],date_of_post=datetime.now())
    p.orders.append(orders_products(buyer_details=user_details(user_id=1,user_name="sreeja",email="a@g.com",phone_number="12345"),date_of_order=datetime.datetime.now(),delivery_status=False,payment_status=False))
    p.save()
    x=product.objects.all()
    return HttpResponse(x)

def new1(request):
    user=request.user

    seller_1 =sellers.objects.filter(seller_details={'user_id':1})[0]

    print(seller_1)
    order_id=1
    product_1=product.objects.filter(seller_details={'user_id':1})[0]
    new_order=orders_sellers(buyer_details=user_details(user_id=user.pk, user_name=user.username, email=user.email,
                                        phone_number=user.mobile))
    new_order.order_id=order_id
    new_order.date_of_order=datetime.datetime.now()
    new_order.told_date_of_order = datetime.datetime.now() + datetime.timedelta(days=int(product_1.product_quantity_available[0]['product_delivery_days']))
    data={}
    data['images']=product_1.images[0]
    data['data']=product_1.product_quantity_available[0]
    data['data']['color']=data['data']['color'][0]
    data['data']['product_title']=product_1.product_title
    data['data']['product_id'] = product_1.pk

    new_order.order_details=[data]
    new_order.quantity = 2
    new_order.payment_status = True
    new_order.delivery_status = False

    seller_1.product_orders.append(new_order)

    seller_1.save()

    return HttpResponse(seller_1.product_orders[0].order_details)


