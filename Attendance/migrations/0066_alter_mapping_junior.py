# Generated by Django 4.1.7 on 2023-04-25 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0065_alter_mapping_junior'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapping',
            name='junior',
            field=models.CharField(max_length=255, verbose_name='Junior'),
        ),
    ]