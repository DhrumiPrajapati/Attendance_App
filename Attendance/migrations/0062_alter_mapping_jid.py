# Generated by Django 4.1.7 on 2023-04-21 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0061_rename_att1_attendance_attendance_mapping_jid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapping',
            name='jid',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Attendance.employee'),
        ),
    ]