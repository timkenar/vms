# Generated by Django 5.0.4 on 2024-04-25 08:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0004_remove_host_address_remove_host_available_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='Visitor_image',
            field=models.ImageField(default='default_image.jpg', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 4, 25, 8, 11, 21, 297455)),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='time_in',
            field=models.TimeField(default=datetime.datetime(2024, 4, 25, 8, 11, 21, 297484)),
        ),
    ]
