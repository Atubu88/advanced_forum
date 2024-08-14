# Generated by Django 5.0.7 on 2024-08-14 20:49

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_topic_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='related_topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.topic'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
