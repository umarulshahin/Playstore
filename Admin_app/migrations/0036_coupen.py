# Generated by Django 4.2.6 on 2024-02-16 14:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_app', '0035_alter_category_options_alter_offer_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('offer_valid_amount', models.IntegerField()),
                ('discount', models.IntegerField()),
                ('created_date', models.DateField(default=django.utils.timezone.now)),
                ('is_delete', models.BooleanField(default=False)),
            ],
        ),
    ]
