# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Comment(models.Model):
    id = models.CharField(max_length=255, blank=True, null=True)
    comment_user_id = models.CharField(max_length=255, blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    weibo_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    crawl_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Frequency(models.Model):
    frequency_value = models.FloatField(blank=True, null=True)
    frequency_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'frequency'


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
    is_blogger = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'information'


class MyUser(models.Model):
    phone = models.CharField(primary_key=True, max_length=11)
    register_time = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    nick_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'my_user'


class Observer(models.Model):
    user_id = models.CharField(max_length=255, blank=True, null=True)
    my_id = models.CharField(max_length=11, blank=True, null=True)
    add_time = models.DateTimeField(blank=True, null=True)
    crawl_time = models.DateTimeField(blank=True, null=True)
    crawl_count = models.BigIntegerField(blank=True, null=True)
    is_exist = models.IntegerField(blank=True, null=True)
    weibo_crawl_time = models.DateTimeField(blank=True, null=True)
    weibo_crawl_count = models.BigIntegerField(blank=True, null=True)
    frequency = models.ForeignKey(Frequency, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'observer'


class PredictUserFeature(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    user_sum_weibo = models.BigIntegerField(blank=True, null=True)
    user_sum_interact = models.BigIntegerField(blank=True, null=True)
    user_avg_interact = models.BigIntegerField(blank=True, null=True)
    user_sum_forward = models.BigIntegerField(blank=True, null=True)
    user_sum_like = models.BigIntegerField(blank=True, null=True)
    user_sum_comment = models.BigIntegerField(blank=True, null=True)
    user_percent_forward = models.BigIntegerField(blank=True, null=True)
    user_percent_comment = models.BigIntegerField(blank=True, null=True)
    user_percent_like = models.BigIntegerField(blank=True, null=True)
    user_max_interact = models.BigIntegerField(blank=True, null=True)
    user_min_interact = models.BigIntegerField(blank=True, null=True)
    user_max_comment = models.BigIntegerField(blank=True, null=True)
    user_min_comment = models.BigIntegerField(blank=True, null=True)
    user_avg_comment = models.BigIntegerField(blank=True, null=True)
    user_max_forward = models.BigIntegerField(blank=True, null=True)
    user_min_forward = models.BigIntegerField(blank=True, null=True)
    user_avg_forward = models.BigIntegerField(blank=True, null=True)
    user_max_like = models.BigIntegerField(blank=True, null=True)
    user_min_like = models.BigIntegerField(blank=True, null=True)
    user_avg_like = models.BigIntegerField(blank=True, null=True)
    user_zero_interact = models.BigIntegerField(blank=True, null=True)
    user_level1_weibo = models.BigIntegerField(blank=True, null=True)
    user_level2_weibo = models.BigIntegerField(blank=True, null=True)
    user_level3_weibo = models.BigIntegerField(blank=True, null=True)
    user_level4_weibo = models.BigIntegerField(blank=True, null=True)
    user_level5_weibo = models.BigIntegerField(blank=True, null=True)
    user_percent_level1_weibo = models.BigIntegerField(blank=True, null=True)
    user_percent_level2_weibo = models.BigIntegerField(blank=True, null=True)
    user_percent_level3_weibo = models.BigIntegerField(blank=True, null=True)
    user_percent_level4_weibo = models.BigIntegerField(blank=True, null=True)
    user_percent_level5_weibo = models.BigIntegerField(blank=True, null=True)
    user_percent_zero_interact = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'predict_user_feature'


class PredictWeiboFeature(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    blog_1day_sum_weibo = models.IntegerField(blank=True, null=True)
    blog_3day_sum_weibo = models.IntegerField(blank=True, null=True)
    blog_7day_sum_weibo = models.IntegerField(blank=True, null=True)
    blog_15day_sum_weibo = models.IntegerField(blank=True, null=True)
    blog_30day_sum_weibo = models.IntegerField(blank=True, null=True)
    blog_60day_sum_weibo = models.IntegerField(blank=True, null=True)
    blog_7day_sum_days = models.IntegerField(blank=True, null=True)
    blog_15day_sum_days = models.IntegerField(blank=True, null=True)
    blog_30day_sum_days = models.IntegerField(blank=True, null=True)
    blog_60day_sum_days = models.IntegerField(blank=True, null=True)
    blog_7day_avg_weibo = models.FloatField(blank=True, null=True)
    blog_15day_avg_weibo = models.FloatField(blank=True, null=True)
    blog_30day_avg_weibo = models.FloatField(blank=True, null=True)
    blog_60day_avg_weibo = models.FloatField(blank=True, null=True)
    blog_1_8hour_sum_weibo = models.BigIntegerField(blank=True, null=True)
    blog_9_17hour_sum_weibo = models.BigIntegerField(blank=True, null=True)
    blog_18_0hour_sum_weibo = models.BigIntegerField(blank=True, null=True)
    blog_weekend_sum_weibo = models.BigIntegerField(blank=True, null=True)
    blog_week1_sum_weibo = models.BigIntegerField(blank=True, null=True)
    blog_week2_sum_weibo = models.BigIntegerField(blank=True, null=True)
    blog_week3_sum_weibo = models.BigIntegerField(blank=True, null=True)
    blog_week4_sum_weibo = models.BigIntegerField(blank=True, null=True)
    blog_week5_sum_weibo = models.BigIntegerField(blank=True, null=True)
    blog_1_8hour_percent_weibo = models.FloatField(blank=True, null=True)
    blog_9_17hour_percent_weibo = models.FloatField(blank=True, null=True)
    blog_18_0hour_percent_weibo = models.FloatField(blank=True, null=True)
    blog_weekend_percent_weibo = models.FloatField(blank=True, null=True)
    blog_week1_percent_weibo = models.FloatField(blank=True, null=True)
    blog_week2_percent_weibo = models.FloatField(blank=True, null=True)
    blog_week3_percent_weibo = models.FloatField(blank=True, null=True)
    blog_week4_percent_weibo = models.FloatField(blank=True, null=True)
    blog_week5_percent_weibo = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'predict_weibo_feature'


class PredictWeiboResult(models.Model):
    id = models.ForeignKey('Weibo', models.DO_NOTHING, db_column='id', primary_key=True)
    like_num = models.IntegerField(blank=True, null=True)
    repost_num = models.IntegerField(blank=True, null=True)
    comment_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'predict_weibo_result'


class Relationship(models.Model):
    id = models.CharField(max_length=255, blank=True, null=True)
    fan_id = models.CharField(max_length=255, blank=True, null=True)
    followed_id = models.CharField(max_length=255, blank=True, null=True)
    crawl_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'relationship'


class UserDailyNum(models.Model):
    weibo_num = models.BigIntegerField(blank=True, null=True)
    follows_num = models.BigIntegerField(blank=True, null=True)
    fans_num = models.BigIntegerField(blank=True, null=True)
    crawl_time = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(Information, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
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
        managed = False
        db_table = 'weibo'


class WeiboDailyNum(models.Model):
    id = models.BigAutoField(primary_key=True)
    like_num = models.BigIntegerField(blank=True, null=True)
    repost_num = models.BigIntegerField(blank=True, null=True)
    comment_num = models.BigIntegerField(blank=True, null=True)
    weibo = models.ForeignKey(Weibo, models.DO_NOTHING, blank=True, null=True)
    crawl_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weibo_daily_num'
