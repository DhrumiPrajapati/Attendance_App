# Generated by Django 4.1.7 on 2023-04-04 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0005_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
