# Generated by Django 2.1.7 on 2019-03-18 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0016_auto_20190316_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='information',
            name='is_blogger',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]