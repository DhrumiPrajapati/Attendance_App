# Generated by Django 4.1.7 on 2023-04-25 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0064_remove_attendance_junior'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapping',
            name='junior',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='name', to='Attendance.employee'),
        ),
    ]