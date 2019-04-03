# Generated by Django 2.1.7 on 2019-03-18 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('selfInfo', '0002_observer_is_exist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Information',
            fields=[
                ('field_id', models.CharField(db_column='_id', max_length=255, primary_key=True, serialize=False)),
                ('nick_name', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(blank=True, max_length=255, null=True)),
                ('province', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('brief_introduction', models.CharField(blank=True, max_length=255, null=True)),
                ('birthday', models.CharField(blank=True, max_length=255, null=True)),
                ('weibo_num', models.IntegerField(blank=True, null=True)),
                ('follows_num', models.IntegerField(blank=True, null=True)),
                ('fans_num', models.IntegerField(blank=True, null=True)),
                ('sex_orientation', models.CharField(blank=True, max_length=255, null=True)),
                ('sentiment', models.CharField(blank=True, max_length=255, null=True)),
                ('vip_level', models.CharField(blank=True, max_length=255, null=True)),
                ('authentication', models.CharField(blank=True, max_length=255, null=True)),
                ('person_url', models.CharField(blank=True, max_length=255, null=True)),
                ('crawl_time', models.CharField(blank=True, max_length=255, null=True)),
                ('labels', models.CharField(blank=True, max_length=255, null=True)),
                ('portrait', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'information',
            },
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('phone', models.CharField(max_length=11, primary_key=True, serialize=False)),
                ('register_time', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('nick_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'my_user',
            },
        ),
        migrations.CreateModel(
            name='UserDailyNum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weibo_num', models.BigIntegerField(blank=True, null=True)),
                ('follows_num', models.BigIntegerField(blank=True, null=True)),
                ('fans_num', models.BigIntegerField(blank=True, null=True)),
                ('crawl_time', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='selfInfo.Information')),
            ],
            options={
                'db_table': 'user_daily_num',
            },
        ),
        migrations.CreateModel(
            name='Weibo',
            fields=[
                ('field_id', models.CharField(db_column='_id', max_length=255, primary_key=True, serialize=False)),
                ('weibo_url', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.CharField(blank=True, max_length=255, null=True)),
                ('like_num', models.IntegerField(blank=True, null=True)),
                ('repost_num', models.IntegerField(blank=True, null=True)),
                ('comment_num', models.IntegerField(blank=True, null=True)),
                ('content', models.CharField(blank=True, max_length=255, null=True)),
                ('crawl_time', models.DateTimeField(blank=True, null=True)),
                ('created_date', models.CharField(blank=True, max_length=255, null=True)),
                ('last_pic_url', models.CharField(blank=True, max_length=255, null=True)),
                ('pic_url', models.CharField(blank=True, max_length=255, null=True)),
                ('crawl_count', models.BigIntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='selfInfo.Information')),
            ],
            options={
                'db_table': 'weibo',
            },
        ),
        migrations.CreateModel(
            name='WeiboDailyNum',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('like_num', models.BigIntegerField(blank=True, null=True)),
                ('repost_num', models.BigIntegerField(blank=True, null=True)),
                ('comment_num', models.BigIntegerField(blank=True, null=True)),
                ('crawl_time', models.DateTimeField(blank=True, null=True)),
                ('weibo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='selfInfo.Weibo')),
            ],
            options={
                'db_table': 'weibo_daily_num',
            },
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='observer',
            name='weibo_crawl_count',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='observer',
            name='weibo_crawl_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='observer',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]