# Generated by Django 4.2.6 on 2024-02-10 04:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_app', '0023_alter_order_items_sub_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sub_category',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_app.category'),
        ),
    ]