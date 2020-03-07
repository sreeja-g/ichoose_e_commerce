from django.urls import path
from .views import *
urlpatterns = [
    path('isell/home/', isell_home, name='isell_home'),
    path('isell/add_products/', add_products, name='add_products'),
    path('isell/add_new_product/', add_new_product, name='add_new_product'),
    path('isell/delivered_products/', delivered_products, name='delivered_products'),
    path('isell/applied_loans/', applied_loans, name='applied_loans'),
    path('isell/verification_request/', verification_request, name='verification_request'),
    path('isell/show_product/', show_product, name='show_product'),
    path('isell/edit_product/', edit_product, name='edit_product'),
    path('isell/show_order/', show_order, name='show_order'),
]