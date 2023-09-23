# Generated by Django 4.2.3 on 2023-09-19 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='img_size',
            field=models.ManyToManyField(blank=True, related_name='image_size', to='api.imagesize', verbose_name='Available thumbnail sizes'),
        ),
    ]
