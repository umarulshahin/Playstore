# Generated by Django 4.2.9 on 2024-01-05 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_app', '0007_alter_product_image_alter_product_image_image_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='discound',
            new_name='discount',
        ),
    ]
