# Generated by Django 2.1.7 on 2019-03-16 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0015_auto_20190316_1634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='field_id',
        ),
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
