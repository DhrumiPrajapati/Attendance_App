# Generated by Django 4.1.7 on 2023-04-03 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Attendance', '0003_employee_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(max_length=50, null=True, verbose_name='Email'),
        ),
    ]