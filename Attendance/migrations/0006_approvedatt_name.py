# Generated by Django 4.1.7 on 2023-05-15 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Attendance', '0005_remove_approvedatt_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvedatt',
            name='name',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='name', to=settings.AUTH_USER_MODEL),
        ),
    ]
