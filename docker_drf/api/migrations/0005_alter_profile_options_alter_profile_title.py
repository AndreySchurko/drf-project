# Generated by Django 4.2.3 on 2023-09-20 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_image_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['title'], 'verbose_name': 'Account tier', 'verbose_name_plural': 'Account tiers'},
        ),
        migrations.AlterField(
            model_name='profile',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Account tier Title'),
        ),
    ]
