from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('study', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_number', models.CharField(max_length=5, verbose_name='출석확인번호')),
                ('title', models.CharField(max_length=30, verbose_name='출석 제목')),
                ('gather_datetime', models.DateTimeField(verbose_name='모임 날짜와 시간')),
                ('expired_datetime', models.DateTimeField(verbose_name='출석 만료시간')),
                ('attendance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.Group')),
            ],
        ),
        migrations.CreateModel(
            name='AttendConfirm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attend_user', models.CharField(max_length=20)),
                ('arrive_time', models.DateTimeField()),
                ('sub_time', models.IntegerField()),
                ('attend_check', models.CharField(choices=[('지각', '지각'), ('출석', '출석')], default='지각', max_length=20)),
                ('attendconfirm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.Attend')),
            ],
        ),
    ]
