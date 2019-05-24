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


class PredictWeiboResult2(models.Model):
    mid = models.CharField(primary_key=True,max_length=255)
    uid = models.CharField(max_length=255, blank=True, null=True)
    like_count = models.IntegerField(blank=True, null=True)
    forward_count = models.IntegerField(blank=True, null=True)
    comment_count = models.IntegerField(blank=True, null=True)
    like_count_new = models.IntegerField(blank=True, null=True)
    forward_count_new = models.IntegerField(blank=True, null=True)
    comment_count_new = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'predict_weibo_result2'

class PredictWeiboResult0403_2rf(models.Model):
    id = models.ForeignKey('Weibo', models.DO_NOTHING, db_column='id', primary_key=True)
    like_num = models.IntegerField(blank=True, null=True)
    repost_num = models.IntegerField(blank=True, null=True)
    comment_num = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'predict_weibo_result_0403_2rf'

class TrainKeyWordTextRank(models.Model):
    weibo_id = models.CharField(primary_key=True, max_length=255)
    content = models.CharField(max_length=255, blank=True, null=True)
    word = models.CharField(max_length=255, blank=True, null=True)
    weight = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'train_key_word_textrank'

class SentimentWeiboResult0518(models.Model):
    mid = models.CharField(primary_key=True, max_length=255)
    content = models.CharField(max_length=255, blank=True, null=True)
    is_positive = models.IntegerField(blank=True, null=True)
    sentiment_score = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'sentiment_weibo_result0518'

class SentimentWeiboResult051802(models.Model):
    mid = models.CharField(primary_key=True, max_length=255)
    content = models.CharField(max_length=255, blank=True, null=True)
    is_positive = models.IntegerField(blank=True, null=True)
    sentiment_score = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'sentiment_weibo_result051802'


class WeiboTrainDataFeature(models.Model):
    uid = models.TextField(blank=True, null=True)
    mid = models.TextField(primary_key=True)
    forward_count = models.BigIntegerField(blank=True, null=True)
    comment_count = models.BigIntegerField(blank=True, null=True)
    like_count = models.BigIntegerField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    hour = models.BigIntegerField(blank=True, null=True)
    weekday = models.BigIntegerField(blank=True, null=True)
    sum_interact = models.BigIntegerField(blank=True, null=True)
    level_interact = models.BigIntegerField(blank=True, null=True)
    blog_15day_sum_days = models.BigIntegerField(blank=True, null=True)
    blog_15day_sum_weibo = models.BigIntegerField(blank=True, null=True)
    blog_1day_sum_weibo = models.BigIntegerField(blank=True, null=True)
    blog_30day_sum_days = models.BigIntegerField(blank=True, null=True)
    blog_30day_sum_weibo = models.BigIntegerField(blank=True, null=True)
    blog_3day_sum_weibo = models.BigIntegerField(blank=True, null=True)
    blog_60day_sum_days = models.BigIntegerField(blank=True, null=True)
    blog_60day_sum_weibo = models.BigIntegerField(blank=True, null=True)
    blog_7day_sum_days = models.BigIntegerField(blank=True, null=True)
    blog_7day_sum_weibo = models.BigIntegerField(blank=True, null=True)
    blog_7day_avg_weibo = models.FloatField(blank=True, null=True)
    blog_15day_avg_weibo = models.FloatField(blank=True, null=True)
    blog_30day_avg_weibo = models.FloatField(blank=True, null=True)
    blog_60day_avg_weibo = models.FloatField(blank=True, null=True)
    blog_1_8hour_sum_weibo = models.IntegerField(db_column='blog_1-8hour_sum_weibo', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    blog_9_17hour_sum_weibo = models.IntegerField(db_column='blog_9-17hour_sum_weibo', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    blog_18_0hour_sum_weibo = models.IntegerField(db_column='blog_18-0hour_sum_weibo', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    blog_weekend_sum_weibo = models.IntegerField(blank=True, null=True)
    blog_week1_sum_weibo = models.IntegerField(blank=True, null=True)
    blog_week2_sum_weibo = models.IntegerField(blank=True, null=True)
    blog_week3_sum_weibo = models.IntegerField(blank=True, null=True)
    blog_week4_sum_weibo = models.IntegerField(blank=True, null=True)
    blog_week5_sum_weibo = models.IntegerField(blank=True, null=True)
    user_mean_of_forward = models.BigIntegerField(blank=True, null=True)
    user_mean_of_comment = models.BigIntegerField(blank=True, null=True)
    user_mean_of_like = models.BigIntegerField(blank=True, null=True)
    user_sum_weibo = models.BigIntegerField(blank=True, null=True)
    user_sum_interact = models.BigIntegerField(blank=True, null=True)
    user_avg_interact = models.FloatField(blank=True, null=True)
    user_sum_forward = models.BigIntegerField(blank=True, null=True)
    user_sum_like = models.BigIntegerField(blank=True, null=True)
    user_sum_comment = models.BigIntegerField(blank=True, null=True)
    user_percent_forward = models.FloatField(blank=True, null=True)
    user_percent_comment = models.FloatField(blank=True, null=True)
    user_percent_like = models.FloatField(blank=True, null=True)
    user_max_interact = models.BigIntegerField(blank=True, null=True)
    user_min_interact = models.BigIntegerField(blank=True, null=True)
    user_max_comment = models.BigIntegerField(blank=True, null=True)
    user_min_comment = models.BigIntegerField(blank=True, null=True)
    user_max_forward = models.BigIntegerField(blank=True, null=True)
    user_min_forward = models.BigIntegerField(blank=True, null=True)
    user_max_like = models.BigIntegerField(blank=True, null=True)
    user_min_like = models.BigIntegerField(blank=True, null=True)
    user_zero_interact = models.FloatField(blank=True, null=True)
    user_level1_weibo = models.FloatField(blank=True, null=True)
    user_level2_weibo = models.FloatField(blank=True, null=True)
    user_level3_weibo = models.FloatField(blank=True, null=True)
    user_level4_weibo = models.FloatField(blank=True, null=True)
    user_level5_weibo = models.FloatField(blank=True, null=True)
    user_percent_level1_weibo = models.FloatField(blank=True, null=True)
    user_percent_level2_weibo = models.FloatField(blank=True, null=True)
    user_percent_level3_weibo = models.FloatField(blank=True, null=True)
    user_percent_level4_weibo = models.FloatField(blank=True, null=True)
    user_percent_level5_weibo = models.FloatField(blank=True, null=True)
    user_percent_zero_interact = models.FloatField(blank=True, null=True)
    blog_1_8hour_percent_weibo = models.FloatField(db_column='blog_1-8hour_percent_weibo', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    blog_9_17hour_percent_weibo = models.FloatField(db_column='blog_9-17hour_percent_weibo', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    blog_18_0hour_percent_weibo = models.FloatField(db_column='blog_18-0hour_percent_weibo', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    blog_weekend_percent_weibo = models.FloatField(blank=True, null=True)
    blog_week1_percent_weibo = models.FloatField(blank=True, null=True)
    blog_week2_percent_weibo = models.FloatField(blank=True, null=True)
    blog_week3_percent_weibo = models.FloatField(blank=True, null=True)
    blog_week4_percent_weibo = models.FloatField(blank=True, null=True)
    blog_week5_percent_weibo = models.FloatField(blank=True, null=True)
    http_number = models.BigIntegerField(blank=True, null=True)
    at_number = models.BigIntegerField(blank=True, null=True)
    weibo_topic_number = models.BigIntegerField(blank=True, null=True)
    is_have_zhuanfa = models.BigIntegerField(blank=True, null=True)
    is_have_dianzan = models.BigIntegerField(blank=True, null=True)
    is_have_emoji = models.BigIntegerField(blank=True, null=True)
    content_length = models.BigIntegerField(blank=True, null=True)
    lda_feature0 = models.FloatField(blank=True, null=True)
    lda_feature1 = models.FloatField(blank=True, null=True)
    lda_feature2 = models.FloatField(blank=True, null=True)
    lda_feature3 = models.FloatField(blank=True, null=True)
    lda_feature4 = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'weibo_train_data_feature'

