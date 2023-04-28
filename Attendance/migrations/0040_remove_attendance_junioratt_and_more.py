# Generated by Django 4.1.7 on 2023-04-20 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0039_alter_mapping_junior'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='junioratt',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='juniors',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='senioratt',
        ),
        migrations.AddField(
            model_name='attendance',
            name='attendance',
            field=models.CharField(choices=[('Full Day', 'Full Day'), ('Half Day', 'Half Day'), ('Overtime', 'Overtime'), ('Absent', 'Absent')], default='Full Day', max_length=100, null=True, verbose_name='My Attendance'),
        ),
    ]
