# Generated by Django 4.1.7 on 2023-04-06 12:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0016_remove_mapping_senior_alter_attendance_tdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapping',
            name='senior',
            field=models.CharField(max_length=100, null=True, verbose_name='Senior'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='tdate',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Today Date'),
        ),
    ]
