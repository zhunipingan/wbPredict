# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
# from django.db import models
#
#
# class TrainData(models.Model):
#     index = models.BigIntegerField(blank=True, null=True)
#     uid = models.TextField(blank=True, null=True)
#     mid = models.TextField(blank=True, null=True)
#     time = models.TextField(blank=True, null=True)
#     date = models.TextField(blank=True, null=True)
#     forward_count = models.BigIntegerField(blank=True, null=True)
#     comment_count = models.BigIntegerField(blank=True, null=True)
#     like_count = models.BigIntegerField(blank=True, null=True)
#     content = models.TextField(blank=True, null=True)
#
#     class Meta:
#         db_table = 'train_data'
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Information(models.Model):
    field_id = models.BigIntegerField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    nick_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    brief_introduction = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.CharField(max_length=255, blank=True, null=True)
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

    class Meta:
        db_table = 'information'


class Weibo(models.Model):
    field_id = models.CharField(db_column='_id', max_length=255, blank=True, null=False,primary_key=True)  # Field renamed because it started with '_'.
    weibo_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.CharField(max_length=255, blank=True, null=True)
    like_num = models.IntegerField(blank=True, null=True)
    repost_num = models.IntegerField(blank=True, null=True)
    comment_num = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.CharField(max_length=30, blank=True, null=True)
    crawl_time = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.CharField(max_length=255, blank=True, null=True)
    pic_url = models.CharField(max_length=255, blank=True, null=True)
    last_pic_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'weibo'
# 上面是0314日的index/models