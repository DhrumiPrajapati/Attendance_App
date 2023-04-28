# Generated by Django 4.1.7 on 2023-04-25 07:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Attendance', '0079_alter_mapping_jid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapping',
            name='jid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to=settings.AUTH_USER_MODEL),
        ),
    ]