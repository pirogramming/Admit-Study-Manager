from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=20, unique=True)),
                ('group_code', models.CharField(max_length=20)),
                ('invitation_url', models.CharField(default=uuid.uuid1, max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('MANAGER', 'MANAGER'), ('MEMBER', 'MEMBER')], default='MEMBER', max_length=20)),
                ('status', models.CharField(choices=[('NEEDS_APPROVAL', 'NEEDS_APPROVAL'), ('ACTIVE', 'ACTIVE'), ('OUT', 'OUT')], default='ACTIVE', max_length=20)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.Group')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='group_member',
            field=models.ManyToManyField(through='study.Membership', to=settings.AUTH_USER_MODEL),
        ),
    ]
