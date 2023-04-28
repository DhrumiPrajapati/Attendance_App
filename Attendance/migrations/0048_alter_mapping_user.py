# Generated by Django 4.1.7 on 2023-04-21 05:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Attendance', '0047_alter_mapping_junior'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapping',
            name='user',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
