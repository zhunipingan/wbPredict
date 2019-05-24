# Generated by Django 2.1.7 on 2019-04-03 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0017_information_is_blogger'),
    ]

    operations = [
        migrations.CreateModel(
            name='PredictWeiboResult',
            fields=[
                ('id', models.ForeignKey(db_column='id', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='index.Weibo')),
                ('like_num', models.IntegerField(blank=True, null=True)),
                ('repost_num', models.IntegerField(blank=True, null=True)),
                ('comment_num', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'predict_weibo_result',
            },
        ),
        migrations.CreateModel(
            name='PredictWeiboResult2',
            fields=[
                ('mid', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('uid', models.CharField(blank=True, max_length=255, null=True)),
                ('like_count', models.IntegerField(blank=True, null=True)),
                ('forward_count', models.IntegerField(blank=True, null=True)),
                ('comment_count', models.IntegerField(blank=True, null=True)),
                ('like_count_new', models.IntegerField(blank=True, null=True)),
                ('forward_count_new', models.IntegerField(blank=True, null=True)),
                ('comment_count_new', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'predict_weibo_result2',
            },
        ),
        migrations.RemoveField(
            model_name='comment',
            name='weibo_url',
        ),
        migrations.AddField(
            model_name='comment',
            name='weibo_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]