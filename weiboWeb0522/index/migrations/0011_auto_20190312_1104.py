# Generated by Django 2.1.7 on 2019-03-12 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0010_information_weibo'),
    ]

    operations = [
        migrations.AddField(
            model_name='weibo',
            name='last_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='weibo',
            name='pic_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
