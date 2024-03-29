# Generated by Django 4.2.6 on 2024-02-09 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_app', '0022_order_items_sub_category_alter_order_items_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_items',
            name='Sub_Category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Admin_app.sub_category'),
        ),
        migrations.AlterField(
            model_name='order_items',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Admin_app.product'),
        ),
    ]
