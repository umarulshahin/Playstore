# Generated by Django 4.2.6 on 2024-02-20 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0008_alter_customuser_options_alter_user_address_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='rafferal_code',
            field=models.CharField(default='old_users12', max_length=100),
            preserve_default=False,
        ),
    ]
