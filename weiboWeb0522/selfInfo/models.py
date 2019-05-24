# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse


# class Comment(models.Model):
#     id = models.CharField(max_length=255, blank=True, null=True)
#     comment_user_id = models.CharField(max_length=255, blank=True, null=True)
#     content = models.CharField(max_length=255, blank=True, null=True)
#     weibo_url = models.CharField(max_length=255, blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     crawl_time = models.DateTimeField(blank=True, null=True)
#
#     class Meta:
#         db_table = 'comment'


class Information(models.Model):
    field_id = models.CharField(db_column='_id', primary_key=True, max_length=255)  # Field renamed because it started with '_'.
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


class MyUser(models.Model):
    phone = models.CharField(primary_key=True, max_length=11)
    self_intro = models.CharField(max_length=30, blank=True, null=True)
    register_time = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    nick_name = models.CharField(max_length=255, blank=True, null=True)
    #0522 修改上传头像
    # img_url = models.ImageField(upload_to='img')  # upload_to指定图片上传的途径，如果不存在则自动创建

    class Meta:
        db_table = 'my_user'


class Frequency(models.Model):
    frequency_value = models.FloatField(blank=True, null=True)
    frequency_id = models.IntegerField(primary_key=True)

    class Meta:
        db_table = 'frequency'


class Observer(models.Model):
    user_id = models.CharField(max_length=255, blank=True, null=True)
    my_id = models.CharField(max_length=11,blank=True, null=True)
    add_time = models.DateTimeField(blank=True, null=True)
    crawl_time = models.DateTimeField(blank=True, null=True)
    crawl_count = models.BigIntegerField(blank=True, null=True)
    is_exist = models.IntegerField(blank=True, null=True)
    weibo_crawl_time = models.DateTimeField(blank=True, null=True)
    weibo_crawl_count = models.BigIntegerField(blank=True, null=True)
    frequency = models.ForeignKey(Frequency, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'observer'

    def get_absolute_url(self):
        return reverse('self:deleteObserver', kwargs={'id': self.id})

    def get_absolute_url2(self):
        return reverse('index:userInfo', kwargs={'userId': self.user_id})



# class Relationship(models.Model):
#     id = models.CharField(max_length=255, blank=True, null=True)
#     fan_id = models.CharField(max_length=255, blank=True, null=True)
#     followed_id = models.CharField(max_length=255, blank=True, null=True)
#     crawl_time = models.DateTimeField(blank=True, null=True)
#
#     class Meta:
#         db_table = 'relationship'


class UserDailyNum(models.Model):
    weibo_num = models.BigIntegerField(blank=True, null=True)
    follows_num = models.BigIntegerField(blank=True, null=True)
    fans_num = models.BigIntegerField(blank=True, null=True)
    crawl_time = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(Information, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'user_daily_num'


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

class Img(models.Model):
    user_phone = models.CharField(primary_key=True, max_length=11)
    img_url = models.ImageField(upload_to='img') # upload_to指定图片上传的途径，如果不存在则自动创建
    class Meta:
        db_table = 'img'

