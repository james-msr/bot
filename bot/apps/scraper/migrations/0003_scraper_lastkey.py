# Generated by Django 3.2.4 on 2021-06-17 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_scraper_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='scraper',
            name='lastkey',
            field=models.CharField(max_length=50, null=True, verbose_name='Last key'),
        ),
    ]
