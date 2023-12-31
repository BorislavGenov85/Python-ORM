# Generated by Django 4.2.4 on 2023-10-24 10:03
import random

from django.db import migrations


def add_barcode(apps, schema_editor):
    Product = apps.get_model("main_app", "Product")
    all_products = Product.objects.all()
    all_barcodes = random.sample(
        range(100000000, 1000000000),
        len(all_products)
    )
    for i in range(len(all_products)):
        product = all_products[i]
        product.barcode = all_barcodes[i]
        product.save()


def reverse_barcode_add(apps, schema_editor):
    Product = apps.get_model('main_app', 'Product')
    for product in Product.objects.all():
        product.barcode = 0
        product.save()


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0004_remove_product_count_product_barcode"),
    ]

    operations = [
        migrations.RunPython(add_barcode, reverse_code=reverse_barcode_add)
    ]
