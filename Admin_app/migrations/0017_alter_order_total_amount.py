# Generated by Django 4.2.9 on 2024-01-30 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_app', '0016_alter_order_status_alter_order_total_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.CharField(max_length=100),
        ),
    ]