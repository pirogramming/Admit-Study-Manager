# Generated by Django 2.2.4 on 2019-08-21 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0003_auto_20190817_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='bio_open',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='membership',
            name='phone_number_open',
            field=models.BooleanField(default=False),
        ),
    ]
