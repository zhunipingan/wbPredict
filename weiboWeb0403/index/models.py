# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse

class Information(models.Model):
    field_id = models.CharField(db_column='_id', primary_key=True, max_length=255)  # Field renamed because it started with '_'.
    nick_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    brief_introduction = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)#CharField(max_length=255, blank=True, null=True)
    weibo_num = models.IntegerField(blank=True, null=True)
    follows_num = models.IntegerField(blank=True, null=True)
    fans_num = models.IntegerField(blank=True, null=True)
    sex_orientation = models.CharField(max_length=255, blank=True, null=True)
    sentiment = models.CharField(max_length=255, blank=True, null=True)
    vip_level = models.CharField(max_length=255, blank=True, null=True)
    authentication = models.CharField(max_length=255, blank=True, null=True)
    person_url = models.CharField(max_length=255, blank=True, null=True)
    crawl_time = models.CharField(max_length=255, blank=True, null=True)
    labels = models.CharField(max_length=255, blank=True, null=True)
    portrait = models.CharField(max_length=255, blank=True, null=True)
    is_blogger = models.IntegerField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('index:userInfo', kwargs={'userId': self.field_id})

    def get_absolute_url_blogger_visual(self):
        return reverse('index:bloggerVisual', kwargs={'bloggerId': self.field_id})

    class Meta:
        db_table = 'information'


class Weibo(models.Model):
    field_id = models.CharField(db_column='_id', primary_key=True, max_length=255)  # Field renamed because it started with '_'.
    weibo_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.CharField(max_length=255, blank=True, null=True)
    like_num = models.IntegerField(blank=True, null=True)
    repost_num = models.IntegerField(blank=True, null=True)
    comment_num = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Information, models.DO_NOTHING, blank=True, null=True)
    crawl_time = models.DateTimeField(blank=True, null=True)
    created_date = models.CharField(max_length=255, blank=True, null=True)
    last_pic_url = models.CharField(max_length=255, blank=True, null=True)
    pic_url = models.CharField(max_length=255, blank=True, null=True)
    crawl_count = models.BigIntegerField(blank=True, null=True)


    def get_absolute_url(self):
        return reverse('index:weiboVisual', kwargs={'weiboId': self.field_id})

    class Meta:
        db_table = 'weibo'


class WeiboDailyNum(models.Model):
    id = models.BigAutoField(primary_key=True)
    like_num = models.BigIntegerField(blank=True, null=True)
    repost_num = models.BigIntegerField(blank=True, null=True)
    comment_num = models.BigIntegerField(blank=True, null=True)
    weibo = models.ForeignKey(Weibo, models.DO_NOTHING, blank=True, null=True)
    crawl_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'weibo_daily_num'


# class Observer(models.Model):
#     user_id = models.CharField(max_length=255, blank=True, null=True)
#     my_id = models.IntegerField(blank=True, null=True)
#     add_time = models.DateTimeField(blank=True, null=True)
#     crawl_time = models.DateTimeField(blank=True, null=True)
#     crawl_count = models.BigIntegerField(blank=True, null=True)
#     is_exist = models.IntegerField(blank=True, null=True)
#     weibo_crawl_time = models.DateTimeField(blank=True, null=True)
#     weibo_crawl_count = models.BigIntegerField(blank=True, null=True)
#
#     class Meta:
#         db_table = 'observer'


class UserDailyNum(models.Model):
    weibo_num = models.BigIntegerField(blank=True, null=True)
    follows_num = models.BigIntegerField(blank=True, null=True)
    fans_num = models.BigIntegerField(blank=True, null=True)
    crawl_time = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(Information, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'user_daily_num'

class Relationship(models.Model):
    filed_id = models.CharField(max_length=255, blank=True, null=True)
    fan_id = models.CharField(max_length=255, blank=True, null=True)
    followed_id = models.CharField(max_length=255, blank=True, null=True)
    crawl_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'relationship'


class Comment(models.Model):
    id = models.CharField(primary_key=True,max_length=255)
    comment_user_id = models.CharField(max_length=255, blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    weibo_id = models.CharField(max_length=255, blank=True, null=True)
    crawl_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'comment'


class PredictWeiboResult(models.Model):
    id = models.ForeignKey('Weibo', models.DO_NOTHING, db_column='id', primary_key=True)
    like_num = models.IntegerField(blank=True, null=True)
    repost_num = models.IntegerField(blank=True, null=True)
    comment_num = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'predict_weibo_result'



