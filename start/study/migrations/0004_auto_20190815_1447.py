# Generated by Django 2.2.4 on 2019-08-15 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0003_auto_20190815_1445'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membership',
            old_name='nowshow_assgin',
            new_name='noshow_assign',
        ),
    ]
