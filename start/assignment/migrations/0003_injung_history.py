# Generated by Django 2.2.4 on 2019-08-15 00:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assignment', '0002_remove_done_noinjung'),
    ]

    operations = [
        migrations.CreateModel(
            name='Injung_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('done', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assignment.Done')),
            ],
        ),
    ]
