# Generated by Django 4.1.7 on 2023-04-25 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0072_alter_mapping_junior'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='names',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Attendance.mapping'),
        ),
    ]