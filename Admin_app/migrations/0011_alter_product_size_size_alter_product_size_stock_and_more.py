# Generated by Django 4.2.9 on 2024-01-27 04:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0006_alter_user_address_phone'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Admin_app', '0010_remove_product_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_size',
            name='size',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product_size',
            name='stock',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=100)),
                ('payment_type', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'processing'), ('shipped', 'shipped'), ('delivered', 'delivered'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('refunded', 'refunded'), ('on_hold', 'on_hold')], default='pending', max_length=100)),
                ('quantity', models.IntegerField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_app.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.user_address')),
            ],
        ),
    ]
