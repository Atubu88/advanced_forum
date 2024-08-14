# Generated by Django 5.0.7 on 2024-08-14 15:03

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_topic_body_remove_topic_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]