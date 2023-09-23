# Generated by Django 4.2.3 on 2023-09-20 14:12

import api.utils
from django.db import migrations
import django_advance_thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_profile_options_alter_profile_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='thumbnail',
            field=django_advance_thumbnail.fields.AdvanceThumbnailField(blank=True, null=True, upload_to=api.utils.get_image_thumb_path),
        ),
    ]
