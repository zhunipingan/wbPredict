# Generated by Django 2.1.7 on 2019-03-13 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0011_auto_20190312_1104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weibo',
            name='last_url',
        ),
        migrations.AddField(
            model_name='weibo',
            name='last_pic_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]