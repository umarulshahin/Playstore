# Generated by Django 4.2.6 on 2024-02-19 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User_Home_app', '0008_wallet_transactions_add_or_pay'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='user_coupon',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='wallet_transactions',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='wishlist',
            options={'ordering': ['-id']},
        ),
    ]
