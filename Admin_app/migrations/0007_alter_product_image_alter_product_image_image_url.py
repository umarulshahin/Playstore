# Generated by Django 4.2.9 on 2024-01-05 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_app', '0006_alter_product_discound'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='img/product'),
        ),
        migrations.AlterField(
            model_name='product_image',
            name='image_url',
            field=models.ImageField(upload_to='img/product'),
        ),
    ]
