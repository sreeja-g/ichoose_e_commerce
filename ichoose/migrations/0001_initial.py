# Generated by Django 2.2.9 on 2020-03-07 09:38

from django.db import migrations, models
import djongo.models.fields
import ichoose.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller_details', djongo.models.fields.EmbeddedField(model_container=ichoose.models.user_details, model_form_class=ichoose.models.user_details_form, null=True)),
                ('product_title', models.TextField()),
                ('category_1', models.TextField()),
                ('category_2', models.TextField()),
                ('product_description', models.TextField()),
                ('images', ichoose.models.CustomListField(default=[])),
                ('product_quantity_available', ichoose.models.CustomListField(default=[])),
                ('additional_information', models.TextField()),
                ('product_customisation_available', ichoose.models.CustomListField(default=[])),
                ('additional_customization_information', models.TextField()),
                ('orders', djongo.models.fields.ArrayField(default=[], model_container=ichoose.models.orders_sellers, model_form_class=ichoose.models.orders_sellers_form)),
                ('date_of_post', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='sellers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller_details', djongo.models.fields.EmbeddedField(model_container=ichoose.models.user_details, model_form_class=ichoose.models.user_details_form, null=True)),
                ('posted_products', djongo.models.fields.ArrayField(default=[], model_container=ichoose.models.product, model_form_class=ichoose.models.product_form)),
                ('product_orders', djongo.models.fields.ArrayField(default=[], model_container=ichoose.models.orders_sellers, model_form_class=ichoose.models.orders_sellers_form)),
            ],
        ),
    ]
