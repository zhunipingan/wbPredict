# Generated by Django 2.1.7 on 2019-05-22 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selfInfo', '0004_auto_20190403_2221'),
    ]

    operations = [
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_url', models.ImageField(upload_to='img')),
            ],
        ),
    ]
