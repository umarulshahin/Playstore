# Generated by Django 4.2.6 on 2024-02-17 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_app', '0037_rename_coupen_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon_discount',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='coupon_valid_amount',
            field=models.IntegerField(null=True),
        ),
    ]
