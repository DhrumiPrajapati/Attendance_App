# Generated by Django 4.1.7 on 2023-04-06 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0014_remove_mapping_senior'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapping',
            name='senior',
            field=models.CharField(max_length=100, null=True, verbose_name='Senior'),
        ),
    ]
