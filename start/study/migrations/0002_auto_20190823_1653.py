# Generated by Django 2.2.4 on 2019-08-23 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='joined_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]