# Generated by Django 4.2.6 on 2024-02-21 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_app', '0039_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['id']},
        ),
    ]
