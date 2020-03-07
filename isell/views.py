from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.urls import reverse
from .models import seller_verification_process
from ichoose.models import user_details,product,sellers
from django.core.files.storage import FileSystemStorage
import json
import datetime

def test_verification(user):
    if user.verification_status==True:
        return True
    else:
        return False

def test_verification_application(user):
    if user.verification_applied==False:
        return True
    else:
        return False


@login_required(login_url='/login/')
def isell_home(request):

    user=request.user
    if user.verification_status==True:
        if len(sellers.objects.filter(seller_details={'user_id': user.pk})) != 1:
            seller_=sellers(
            seller_details=user_details(user_id=user.pk, user_name=user.username, email=user.email,
                                        phone_number=user.mobile))
            seller_.save()
        else:
            seller_=sellers.objects.get(seller_details={'user_id':user.pk})

        orders=seller_.product_orders
        pending_orders=[]

        for each in orders:
            if each.delivery_status==False:
                pending_orders.append(each)

        return render(request,'index3.html',{'pending_orders':pending_orders})
    else:
        return render(request, 'index3.html')

@login_required(login_url='/login/')
@user_passes_test(test_verification_application,login_url='/isell/home/')
def verification_request(request):
    if request.method == 'POST':

        user=request.user

        name = request.POST.get('name')
        ph_number = request.POST.get('ph_number')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        purpose = request.FILES.getlist('purpose')
        images = request.FILES.getlist('images')
        files = request.FILES.getlist('files')

        verification_process = seller_verification_process(seller_details=user_details(user_id=user.pk,user_name=user.username,email=user.email,phone_number=user.mobile))
        verification_process.name=name
        verification_process.phone_number=ph_number
        verification_process.address_line_1=address_line_1
        verification_process.address_line_2=address_line_2
        verification_process.city=city
        verification_process.state=state
        verification_process.pincode=pincode
        verification_process.purpose=purpose

        for each in images:
            fs = FileSystemStorage()
            fs.save('seller_images/'+each.name, each)
            verification_process.images.append('seller_images/'+each.name)

        for each in files:
            fs = FileSystemStorage()
            fs.save('seller_files/' + each.name, each)
            verification_process.files.append('seller_files/' + each.name)

        verification_process.save()
        user.verification_applied=True
        user.save()

        return redirect(reverse('isell:isell_home'))

    else:

        return render(request,'verification_request.html')

@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def add_products(request):

    user=request.user
    products=product.objects.filter(seller_details={'user_id': user.pk})

    return render(request,'add_products.html',{'products':products})


@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def delivered_products(request):
    user = request.user

    if len(sellers.objects.filter(seller_details={'user_id': user.pk})) != 1:
        seller_ = sellers(
            seller_details=user_details(user_id=user.pk, user_name=user.username, email=user.email,
                                        phone_number=user.mobile))
        seller_.save()
    else:
        seller_ = sellers.objects.get(seller_details={'user_id': user.pk})

    orders = seller_.product_orders
    delivered_orders = []

    for each in orders:
        if each.delivery_status == True:
            delivered_orders.append(each)

    return render(request, 'delivered_products.html', {'delivered_orders': delivered_orders})


@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def applied_loans(request):
    return render(request,'applied_loans.html')

@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def add_new_product(request):
    if request.method == 'POST':

        print(json.loads(request.POST.get('data')))

        user = request.user
        data=json.loads(request.POST.get('data'))
        new_product = product(
            seller_details=user_details(user_id=user.pk, user_name=user.username, email=user.email,
                                        phone_number=user.mobile))

        new_product.product_title = data['product_title']
        new_product.product_description = data['product_description']
        new_product.category_1 = data['product_category_1']
        new_product.category_2 = data['product_category_2']
        new_product.additional_information = data['additional_information']
        new_product.additional_customization_information = data['additional_customization_information']
        new_product.save()

        for i in range(0,int(request.POST.get('product_type_images_num'))):
            image_list=[]
            images = request.FILES.getlist('product_type_images_'+str(i))
            print(images)
            for each in images:
                fs = FileSystemStorage()
                fs.save('seller_product_images/' + str(new_product.pk)+"/" + str(i)+"/"+ each.name, each)
                image_list.append('seller_product_images/' + str(new_product.pk)+"/" + str(i)+"/"+ each.name)
                print(image_list)
            print(image_list)
            new_product.images.append(image_list)

        new_product.product_quantity_available = data['product_types']

        new_product.product_customisation_available=[data['customization_types']]
        new_product.date_of_post=datetime.datetime.now()
        new_product.save()


        return redirect(reverse('isell:add_products'))

    else:


        return render(request,'add_product_form.html')



@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def show_product(request):
    product_details=product.objects.get(pk=request.GET.get('product_no'))
    data=zip(product_details.images,product_details.product_quantity_available)
    return render(request,'show_product.html',{'product_details':product_details,'data':data})


@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def edit_product(request):
    if request.method == 'POST':

        print(json.loads(request.POST.get('data')))

        user = request.user
        data=json.loads(request.POST.get('data'))
        new_product = product.objects.get(pk=int(request.POST.get('product_pk')))
        new_product.product_title = data['product_title']
        new_product.product_description = data['product_description']
        new_product.category_1 = data['product_category_1']
        new_product.category_2 = data['product_category_2']
        new_product.additional_information = data['additional_information']
        new_product.additional_customization_information = data['additional_customization_information']
        new_product.save()

        new_product.images=[]
        for i in range(0,int(request.POST.get('product_type_images_num'))):
            image_list=[]
            images = request.FILES.getlist('product_type_images_'+str(i))
            print(images)
            for each in images:
                fs = FileSystemStorage()
                fs.save('seller_product_images/' + str(new_product.pk)+"/" + str(i)+"/"+ each.name, each)
                image_list.append('seller_product_images/' + str(new_product.pk)+"/" + str(i)+"/"+ each.name)
                print(image_list)
            print(image_list)
            new_product.images.append(image_list)

        new_product.product_quantity_available = data['product_types']

        new_product.product_customisation_available=[data['customization_types']]
        new_product.date_of_post=datetime.datetime.now()
        new_product.save()


        return redirect(reverse('isell:add_products'))

    else:

        product_to_edit = product.objects.get(pk=request.GET.get('product_pk'))

        return render(request, 'edit_product_form.html', {'product_to_edit': product_to_edit})


@login_required(login_url='/login/')
@user_passes_test(test_verification,login_url='/isell/home/')
def show_order(request):
    user=request.user
    seller_details=sellers.objects.get(seller_details={'user_id':user.pk})
    order_details={}
    data={}
    for each in seller_details.product_orders:
        if each.order_id==int(request.GET.get('order_pk')):
            order_details=each
    return render(request,'show_order.html',{'order_details':order_details})
