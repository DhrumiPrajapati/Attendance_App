# Generated by Django 4.1.7 on 2023-04-27 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0097_delete_jrattendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='mapping',
            field=models.CharField(max_length=255, null=True, verbose_name='Juniors'),
        ),
    ]
