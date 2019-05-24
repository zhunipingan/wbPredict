from django.shortcuts import render,redirect
from django.db.models import Sum
# Create your views here.
from django.http import HttpResponse
# from .models import TrainData
import datetime
from .models import Weibo
from .models import Information
from .models import WeiboDailyNum
from .models import UserDailyNum,Relationship,Comment,PredictWeiboResult,PredictWeiboResult2
from .models import PredictWeiboResult0403_2rf,TrainKeyWordTextRank,SentimentWeiboResult0518,SentimentWeiboResult051802,WeiboTrainDataFeature
from django.db.models.aggregates import Count
import numpy as np

from django.db.models import F,Q
from django.db.models.functions.datetime import TruncMonth,TruncYear
import jieba
import codecs
import collections # 词频统计库
import json
#0320 分页 博主主页
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage

def weiboVisual(request,weiboId):
    userId = weiboId.split('_')[0]
    #博主的微博list
    weibo_list = Weibo.objects.filter(Q(user = userId) & ~Q(field_id = weiboId)).order_by('-created_at')
    #0509修改 添加该条微博信息
    weibo_info = Weibo.objects.filter(field_id = weiboId)

    #微博每日互动量信息
    weibo_daily_list = WeiboDailyNum.objects.filter(weibo = weiboId).order_by('crawl_time')
    # weibo_pie = weibo_daily_list.aggregate(like = Sum('like_num'),forward = Sum('repost_num'), comment= Sum('comment_num'))#.values('like','forward','comment')
    res_dict = {}
    # res_dict = {'日期': list, '点赞数': list, '转发数' :list,'评论数':list}
    date_list = []
    forward_list = []
    like_list = []
    comment_list = []
    for element in weibo_daily_list:
        date_list.append(str(element.crawl_time))
        forward_list.append(element.repost_num)
        like_list.append(element.like_num)
        comment_list.append(element.comment_num)
        # res_dict['日期'] = res_dict['日期'].append(element.time)
        # res_dict['点赞数'] = res_dict['点赞数'].append(element.like_count)
        # res_dict['转发数'] = res_dict['转发数'].append(element.forward_count)
        # res_dict['评论数'] = res_dict['评论数'].append(element.comment_count)


    res_dict['date'] = date_list
    res_dict['like'] = like_list
    res_dict['forward'] = forward_list
    res_dict['comment'] = comment_list

    weibo_pie = weibo_daily_list.last()
    pie_info2 = []
    if weibo_pie is None:
        pie_info2 = [{'name':'点赞数','value':0,'percent':0},{'name':'转发数','value':0,'percent':0},{'name':'评论数','value':0,'percent':0}]
        pie_info = {
            'like': 0,
            'forward': 0,
            'comment': 0  # weibo_pie['comment']
        }
    else:
        pie_sum = int(weibo_pie.like_num) + int(weibo_pie.repost_num) + int(weibo_pie.comment_num)
        if pie_sum > 0:
            pie_info2 = [{'name':'点赞数','value':weibo_pie.like_num,'percent':round(weibo_pie.like_num/pie_sum*100,2)},{'name':'转发数','value':weibo_pie.repost_num,
            'percent':round(weibo_pie.repost_num/pie_sum*100,2)},{'name':'评论数','value':weibo_pie.comment_num,'percent':round(weibo_pie.comment_num/pie_sum*100,2)}]
        else:
            pie_info2 = [
                {'name': '点赞数', 'value': weibo_pie.like_num, 'percent': 0},
                {'name': '转发数', 'value': weibo_pie.repost_num,
                 'percent': 0},
                {'name': '评论数', 'value': weibo_pie.comment_num,
                 'percent': 0}]
        pie_info = {
            'like':weibo_pie.like_num,
            'forward':weibo_pie.repost_num,
            'comment':weibo_pie.comment_num#weibo_pie['comment']
        }

    # 评论信息1699432410_HkZIvDKo3
    comment_info_list = Comment.objects.filter(weibo_id=weiboId).order_by('-created_at')
    hot_comment = comment_info_list[:100]
    stop_words_txt = codecs.open(r'D:\graduation project\weiboWeb\extraFile\GlobalStopWords.txt', 'r', encoding='UTF-8').readlines()
    stop_words = [word.strip('\n') for word in stop_words_txt]
    # 0426修改 对于 回复 这个词也不显示
    stop_words.append('回复')
    word_list = []
    for element in comment_info_list:
        content = element.content
        word_list.extend(jieba.cut(content))
    word_list = [x for x in word_list if x.strip() not in stop_words]
    word_counts = collections.Counter(word_list)  # 对分词做词频统计
    word_cloud_list = []
    for element in word_counts:
        word_dict = {}
        word_dict['name'] = element
        word_dict['value'] = word_counts[element]
        word_cloud_list.append(word_dict)

    #个人信息
    information = Information.objects.get(field_id=userId)
    #0509修改
    if len(weibo_info) > 0:
        weibo = weibo_info[0]
        weibo.nick_name = information.nick_name
        weibo.portrait = information.portrait
        pic_url = weibo.pic_url.split(',')
        last_pic_url = weibo.last_pic_url.split(',')
        weibo.pic_url = []
        if pic_url != ['']:
            weibo.pic_url = weibo.pic_url + pic_url
            if last_pic_url != ['']:
                weibo.pic_url = weibo.pic_url + last_pic_url
        if last_pic_url != ['']:
            weibo.pic_url = weibo.pic_url + last_pic_url
    else:
        weibo = None
    weibo_key_word = TrainKeyWordTextRank.objects.filter(weibo_id=weiboId)
    if (len(weibo_key_word) > 0):
        weibo.key_word = weibo_key_word[0].word
        weibo.key_weight = weibo_key_word[0].weight
    else:
        weibo.key_word = ''
        weibo.key_weight = ''
    weibo.key_word = weibo.key_word.split(',')
    weibo.key_weight = weibo.key_weight.split(',')
    weibo.key = list(zip(weibo.key_word,weibo.key_weight))
    # 情感分析
    weibo_sentiment_info = SentimentWeiboResult051802.objects.filter(mid=weiboId)
    if (len(weibo_sentiment_info) > 0):
        negative_score = round(float(weibo_sentiment_info[0].sentiment_score.split(',')[0]) * 100,2)
    else:
        negative_score = 50

        # element.pic_url = ['http://wx2.sinaimg.cn/wap180/006dWiXzly1fpde9eihxyj31kw1kwkjl.jpg']
    return render(request, 'index/weibo_visual4.html',{'negative_score':negative_score,'list':res_dict,'pie':pie_info,'pie2':pie_info2,'word_cloud':word_cloud_list,'user_info':information,'hot_comment':hot_comment,'weibo_list':weibo_list,'weibo':weibo})#'user_info':user_info


def userInfo(request,userId):
    weibo = Weibo.objects.filter(user = userId).order_by('-created_at') #user_id
    information = Information.objects.get(field_id = userId)
    # return HttpResponse(information.fans_num)

    if information:
        if information.city == 'None':
            information.city = ''
        if information.gender == 'None':
            information.gender = '保密'
        if information.birthday == 'None':
            information.birthday = '保密'
        if information.sex_orientation == 'None':
            information.sex_orientation = '保密'
        if information.labels == 'None':
            information.labels = '无'
        user_info = {
            'name':information.nick_name,
            'introduction':information.brief_introduction,
            'fans':information.fans_num,
            'follows':information.follows_num,
            'blogs':information.weibo_num,
            'gender':information.gender,
            'location':information.province + ' ' + information.city,
            'birthday':information.birthday,
            'sex_orientation':information.sex_orientation,
            'labels':information.labels,
            'portrait':information.portrait,
            'id':information.field_id
        }
    else:
        user_info = {
            'name': 'ERROR',
            'introduction': 'ERROR',
            'fans': 0,
            'follows': 0,
            'blogs': 0
        }
    #0320 进行微博显示的分页
    # weibo_info = weibo[:10]
    # for element in weibo_info:
    #     pic_url = element.pic_url.split(',')
    #     last_pic_url = element.last_pic_url.split(',')
    #     element.pic_url = []
    #     if pic_url != ['']:
    #         element.pic_url = element.pic_url + pic_url
    #         if last_pic_url != ['']:
    #             element.pic_url = element.pic_url + last_pic_url
    #     if last_pic_url != ['']:
    #         element.pic_url = element.pic_url + last_pic_url

    paginator = Paginator(weibo, 10)
    try:
        page_number = request.GET.get('page', '1')
        page = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage, InvalidPage):
        # 如果出现上述异常，默认展示第1页
        page = paginator.page(1)
    for element in page.object_list:
        pic_url = element.pic_url.split(',')
        last_pic_url = element.last_pic_url.split(',')
        element.pic_url = []
        if pic_url != ['']:
            element.pic_url = element.pic_url + pic_url
            if last_pic_url != ['']:
                element.pic_url = element.pic_url + last_pic_url
        if last_pic_url != ['']:
            element.pic_url = element.pic_url + last_pic_url
        # element.pic_url = ['http://wx2.sinaimg.cn/wap180/006dWiXzly1fpde9eihxyj31kw1kwkjl.jpg']
    return render(request, 'index/user_info2.html',{'user_info':user_info,'page': page})#'user_weibo':weibo_info,



def bloggerVisual(request,bloggerId):
    information = Information.objects.get(field_id=bloggerId)

    user_info_list = UserDailyNum.objects.filter(user = bloggerId).order_by('crawl_time')
    res_dict = {}
    weibo_num_list = []
    fans_num_list = []
    follows_num_list = []
    date_list = []
    for element in user_info_list:
        weibo_num_list.append(str(element.weibo_num))
        fans_num_list.append(element.fans_num)
        follows_num_list.append(element.follows_num)
        date_list.append(str(element.crawl_time))

    res_dict['date_list'] = date_list
    res_dict['weibo_num_list'] = weibo_num_list
    res_dict['fans_num_list'] = fans_num_list
    res_dict['follows_num_list'] = follows_num_list
    res_dict['date_list_diff'] = date_list[:-1]
    res_dict['daily_fans_diff'] = list(np.diff(fans_num_list))

    fans_id_list = Relationship.objects.filter(followed_id = bloggerId).values('fan_id')
    fans_info_list = Information.objects.filter(field_id__in = fans_id_list)
    #地域分布
    location_group = fans_info_list.values('province').annotate(name=F('province'),value = Count('field_id')).values('name','value')
    # print(list(location_group))
    location_list = list(location_group)
    province_list = ['北京','天津','上海','重庆','河北','山西','辽宁','吉林','黑龙江','江苏','浙江','安徽','福建','江西',
                     '山东','河南','湖北','湖南','广东','海南','四川','贵州','云南','陕西','甘肃','青海','台湾',
                     '内蒙古','广西','西藏','宁夏','新疆','香港','澳门']
    location_list = [element for element in location_list if element['name'] in province_list]
    #性别分布
    sex_group = fans_info_list.values('gender').annotate(value = Count('field_id'))

    sex_info = []
    for element in sex_group:
        if element['gender'] != 'None':
            sex_dict = dict()
            sex_dict['name'] = element['gender']
            sex_dict['value'] = int(element['value'])
            sex_info.append(sex_dict)
    #年龄分布0324修改，年份0000不属于正常年份
    now_year = datetime.datetime.now().year
    age_group = fans_info_list.filter(birthday__regex="^(?!0000)\d{4}-\d{1,2}-\d{1,2}").annotate(date = TruncYear('birthday')).values('date')#.annotate(values = Count('field_id'))
    age_list = [(now_year - age['date'].year)//20 for age in age_group ]
    age_info = []
    age_name_info = []
    for i in set(age_list):
        age_dict = {}
        if i < 5:
            age_dict['name'] = str(i*20)+'-'+str(i*20+19)+'岁'
            age_name_info.append(age_dict['name'])
            age_dict['value'] = age_list.count(i)
            age_info.append(age_dict)

    #0327 visual3增加了博主历史所有微博互动量统计，加入预测对比
    #微博每日互动量信息
    weibo_daily_list = Weibo.objects.filter(user = bloggerId).order_by('created_at')
    # weibo_pie = weibo_daily_list.aggregate(like = Sum('like_num'),forward = Sum('repost_num'), comment= Sum('comment_num'))#.values('like','forward','comment')
    weibo_res_dict = {}
    # res_dict = {'日期': list, '点赞数': list, '转发数' :list,'评论数':list}
    date_list = []
    forward_list = []
    like_list = []
    comment_list = []
    predict_forward_list = []
    predict_like_list = []
    predict_comment_list = []
    # weibo_predict_list = PredictWeiboResult.objects.filter(id__in=weibo_daily_list.values_list('field_id',flat=True))
    # print('1111111111',weibo_predict_list[0])
    for element in weibo_daily_list:
        weibo_predict_info = PredictWeiboResult0403_2rf.objects.filter(id = element.field_id)
        if len(weibo_predict_info) > 0:
            predict_comment_list.append(weibo_predict_info[0].comment_num)
            predict_like_list.append(weibo_predict_info[0].like_num)
            predict_forward_list.append(weibo_predict_info[0].repost_num)
        else:
            predict_comment_list.append(0)
            predict_like_list.append(0)
            predict_forward_list.append(0)
        date_list.append(str(element.created_at))
        forward_list.append(element.repost_num)
        like_list.append(element.like_num)
        comment_list.append(element.comment_num)
        # res_dict['日期'] = res_dict['日期'].append(element.time)
        # res_dict['点赞数'] = res_dict['点赞数'].append(element.like_count)
        # res_dict['转发数'] = res_dict['转发数'].append(element.forward_count)
        # res_dict['评论数'] = res_dict['评论数'].append(element.comment_count)

    # weibo_res_dict['predict_date'] = list(weibo_predict_list.values_list('created_at',flat=True))
    weibo_res_dict['predict_like'] = predict_like_list#list(weibo_predict_list.values_list('like_num',flat=True))
    weibo_res_dict['predict_comment'] = predict_comment_list
    weibo_res_dict['predict_forward'] = predict_forward_list
    weibo_res_dict['date'] = date_list
    weibo_res_dict['like'] = like_list
    weibo_res_dict['forward'] = forward_list
    weibo_res_dict['comment'] = comment_list

    #0510修改 预测影响因素
    like_factor = [(0.3152, 'user_mean_of_like'), (0.0602, 'lda_feature2'), (0.0599, 'lda_feature1'), (0.0449, 'blog_60day_avg_weibo'), (0.0437, 'lda_feature0'), (0.0393, 'lda_feature4'), (0.0369, 'blog_60day_sum_weibo'), (0.0317, 'lda_feature3'), (0.0301, 'blog_30day_avg_weibo'), (0.0274, 'content_length'), (0.0248, 'http_number'), (0.0229, 'blog_60day_sum_days'), (0.0226, 'blog_1day_sum_weibo'), (0.0216, 'blog_30day_sum_weibo'), (0.017, 'blog_15day_sum_weibo'), (0.0166, 'weekday'), (0.0152, 'is_have_dianzan'), (0.0151, 'blog_15day_avg_weibo'), (0.0148, 'hour'), (0.0137, 'blog_7day_sum_weibo'), (0.0134, 'blog_3day_sum_weibo'), (0.0131, 'blog_30day_sum_days'), (0.0109, 'blog_7day_avg_weibo'), (0.0108, 'user_percent_forward'), (0.0105, 'user_mean_of_comment'), (0.0102, 'blog_15day_sum_days'), (0.0078, 'user_max_like'), (0.0073, 'user_percent_level4_weibo'), (0.0068, 'user_level1_weibo'), (0.0066, 'at_number'), (0.0054, 'user_percent_level3_weibo'), (0.0036, 'blog_7day_sum_days'), (0.0033, 'user_sum_weibo'), (0.0028, 'weibo_topic_number'), (0.0024, 'user_sum_like'), (0.0021, 'is_have_emoji'), (0.0013, 'user_percent_level5_weibo'), (0.0012, 'user_sum_comment'), (0.0011, 'is_have_zhuanfa'), (0.0009, 'user_percent_zero_interact'), (0.0009, 'user_max_forward'), (0.0007, 'user_percent_level2_weibo'), (0.0006, 'user_mean_of_forward'), (0.0005, 'user_max_interact'), (0.0004, 'user_avg_interact'), (0.0002, 'user_zero_interact'), (0.0002, 'user_percent_like'), (0.0002, 'user_percent_level1_weibo'), (0.0002, 'user_percent_comment'), (0.0002, 'blog_weekend_percent_weibo'), (0.0001, 'user_sum_forward'), (0.0001, 'user_max_comment'), (0.0001, 'user_level5_weibo'), (0.0001, 'user_level4_weibo'), (0.0001, 'user_level3_weibo'), (0.0001, 'user_level2_weibo'), (0.0001, 'blog_week2_percent_weibo'), (0.0, 'user_sum_interact'), (0.0, 'user_min_like'), (0.0, 'user_min_interact'), (0.0, 'user_min_forward'), (0.0, 'user_min_comment'), (0.0, 'blog_weekend_sum_weibo'), (0.0, 'blog_week5_sum_weibo'), (0.0, 'blog_week5_percent_weibo'), (0.0, 'blog_week4_sum_weibo'), (0.0, 'blog_week4_percent_weibo'), (0.0, 'blog_week3_sum_weibo'), (0.0, 'blog_week3_percent_weibo'), (0.0, 'blog_week2_sum_weibo'), (0.0, 'blog_week1_sum_weibo'), (0.0, 'blog_week1_percent_weibo'), (0.0, 'blog_9-17hour_sum_weibo'), (0.0, 'blog_9-17hour_percent_weibo'), (0.0, 'blog_18-0hour_sum_weibo'), (0.0, 'blog_18-0hour_percent_weibo'), (0.0, 'blog_1-8hour_sum_weibo'), (0.0, 'blog_1-8hour_percent_weibo')]
    comment_factor = [(0.1211, 'user_mean_of_comment'), (0.1124, 'lda_feature0'), (0.1111, 'lda_feature1'), (0.0797, 'lda_feature2'), (0.059, 'blog_60day_avg_weibo'), (0.0578, 'is_have_dianzan'), (0.0433, 'lda_feature4'), (0.0402, 'blog_30day_avg_weibo'), (0.0364, 'lda_feature3'), (0.0313, 'content_length'), (0.0259, 'blog_3day_sum_weibo'), (0.0201, 'is_have_zhuanfa'), (0.0199, 'blog_1day_sum_weibo'), (0.0185, 'blog_15day_avg_weibo'), (0.0183, 'blog_30day_sum_weibo'), (0.0181, 'weibo_topic_number'), (0.0179, 'blog_60day_sum_weibo'), (0.0163, 'blog_7day_avg_weibo'), (0.0152, 'blog_30day_sum_days'), (0.0113, 'user_max_like'), (0.0113, 'blog_7day_sum_weibo'), (0.0106, 'hour'), (0.0105, 'user_max_comment'), (0.0101, 'blog_15day_sum_days'), (0.01, 'blog_60day_sum_days'), (0.0088, 'user_percent_level1_weibo'), (0.0076, 'http_number'), (0.0075, 'blog_15day_sum_weibo'), (0.0071, 'weekday'), (0.0051, 'user_percent_level5_weibo'), (0.0045, 'blog_7day_sum_days'), (0.0042, 'at_number'), (0.0025, 'user_percent_like'), (0.0024, 'user_level1_weibo'), (0.002, 'user_sum_interact'), (0.0019, 'user_sum_like'), (0.0018, 'user_mean_of_like'), (0.0017, 'user_level2_weibo'), (0.0017, 'blog_weekend_percent_weibo'), (0.0016, 'user_percent_level2_weibo'), (0.0014, 'user_percent_forward'), (0.0013, 'blog_9-17hour_percent_weibo'), (0.0012, 'user_sum_forward'), (0.0009, 'user_percent_level4_weibo'), (0.0009, 'user_percent_comment'), (0.0009, 'user_level3_weibo'), (0.0008, 'user_percent_zero_interact'), (0.0007, 'user_max_forward'), (0.0007, 'user_level4_weibo'), (0.0007, 'is_have_emoji'), (0.0006, 'user_max_interact'), (0.0006, 'user_avg_interact'), (0.0005, 'user_percent_level3_weibo'), (0.0005, 'blog_week3_percent_weibo'), (0.0003, 'user_zero_interact'), (0.0002, 'user_mean_of_forward'), (0.0002, 'user_level5_weibo'), (0.0002, 'blog_week1_percent_weibo'), (0.0001, 'user_sum_weibo'), (0.0001, 'user_sum_comment'), (0.0001, 'blog_week4_percent_weibo'), (0.0001, 'blog_week2_percent_weibo'), (0.0001, 'blog_18-0hour_percent_weibo'), (0.0, 'user_min_like'), (0.0, 'user_min_interact'), (0.0, 'user_min_forward'), (0.0, 'user_min_comment'), (0.0, 'blog_weekend_sum_weibo'), (0.0, 'blog_week5_sum_weibo'), (0.0, 'blog_week5_percent_weibo'), (0.0, 'blog_week4_sum_weibo'), (0.0, 'blog_week3_sum_weibo'), (0.0, 'blog_week2_sum_weibo'), (0.0, 'blog_week1_sum_weibo'), (0.0, 'blog_9-17hour_sum_weibo'), (0.0, 'blog_18-0hour_sum_weibo'), (0.0, 'blog_1-8hour_sum_weibo'), (0.0, 'blog_1-8hour_percent_weibo')]
    repost_factor = [(0.1144, 'user_mean_of_forward'), (0.0727, 'content_length'), (0.0541, 'is_have_zhuanfa'), (0.0484, 'lda_feature2'), (0.0483, 'lda_feature0'), (0.0457, 'lda_feature4'), (0.0396, 'blog_60day_avg_weibo'), (0.0388, 'lda_feature3'), (0.0387, 'blog_60day_sum_weibo'), (0.0361, 'lda_feature1'), (0.0316, 'blog_7day_avg_weibo'), (0.0309, 'blog_30day_sum_weibo'), (0.0291, 'blog_15day_avg_weibo'), (0.0278, 'blog_7day_sum_weibo'), (0.024, 'http_number'), (0.0232, 'blog_3day_sum_weibo'), (0.0216, 'blog_30day_avg_weibo'), (0.0214, 'hour'), (0.0192, 'user_level3_weibo'), (0.0191, 'blog_60day_sum_days'), (0.0178, 'blog_1day_sum_weibo'), (0.017, 'weekday'), (0.0159, 'blog_15day_sum_weibo'), (0.0152, 'at_number'), (0.0146, 'user_avg_interact'), (0.0145, 'user_sum_forward'), (0.0138, 'user_percent_comment'), (0.0136, 'user_level2_weibo'), (0.013, 'weibo_topic_number'), (0.0108, 'blog_15day_sum_days'), (0.0101, 'blog_30day_sum_days'), (0.0084, 'user_percent_level3_weibo'), (0.008, 'user_mean_of_comment'), (0.0058, 'blog_7day_sum_days'), (0.0045, 'user_max_interact'), (0.0038, 'user_max_forward'), (0.0027, 'user_percent_level5_weibo'), (0.0025, 'is_have_dianzan'), (0.0021, 'blog_weekend_percent_weibo'), (0.002, 'user_percent_like'), (0.002, 'user_percent_level4_weibo'), (0.0018, 'user_percent_level1_weibo'), (0.0017, 'user_percent_level2_weibo'), (0.0017, 'user_max_comment'), (0.0015, 'user_zero_interact'), (0.0014, 'user_mean_of_like'), (0.0014, 'blog_week4_percent_weibo'), (0.0011, 'user_max_like'), (0.001, 'user_sum_like'), (0.001, 'user_level1_weibo'), (0.0006, 'user_sum_comment'), (0.0006, 'user_percent_forward'), (0.0005, 'user_sum_interact'), (0.0005, 'is_have_emoji'), (0.0004, 'user_percent_zero_interact'), (0.0004, 'blog_9-17hour_percent_weibo'), (0.0003, 'blog_week1_percent_weibo'), (0.0003, 'blog_18-0hour_percent_weibo'), (0.0002, 'user_level5_weibo'), (0.0002, 'user_level4_weibo'), (0.0002, 'blog_week2_percent_weibo'), (0.0001, 'user_sum_weibo'), (0.0001, 'blog_week3_percent_weibo'), (0.0, 'user_min_like'), (0.0, 'user_min_interact'), (0.0, 'user_min_forward'), (0.0, 'user_min_comment'), (0.0, 'blog_weekend_sum_weibo'), (0.0, 'blog_week5_sum_weibo'), (0.0, 'blog_week5_percent_weibo'), (0.0, 'blog_week4_sum_weibo'), (0.0, 'blog_week3_sum_weibo'), (0.0, 'blog_week2_sum_weibo'), (0.0, 'blog_week1_sum_weibo'), (0.0, 'blog_9-17hour_sum_weibo'), (0.0, 'blog_18-0hour_sum_weibo'), (0.0, 'blog_1-8hour_sum_weibo'), (0.0, 'blog_1-8hour_percent_weibo')]
    return render(request, 'index/blogger_visual3.html',{'like_factor':like_factor,'comment_factor':comment_factor,'repost_factor':repost_factor,'weibo_analyse_list':weibo_res_dict,'list':res_dict,'sex_info':sex_info,'location_info':location_list,'foreign_fans_num':len(location_group)-len(location_list),'age_info':age_info,'user_info':information})#'user_info':user_info


def bloggerTianchiVisual(request,bloggerId):

    #0327 visual3增加了博主历史所有微博互动量统计，加入预测对比
    #微博每日互动量信息
    weibo_daily_list = PredictWeiboResult2.objects.filter(uid = bloggerId).order_by('time')
    # weibo_pie = weibo_daily_list.aggregate(like = Sum('like_num'),forward = Sum('repost_num'), comment= Sum('comment_num'))#.values('like','forward','comment')
    weibo_res_dict = {}
    # res_dict = {'日期': list, '点赞数': list, '转发数' :list,'评论数':list}
    date_list = []
    forward_list = []
    like_list = []
    comment_list = []
    predict_forward_list = []
    predict_like_list = []
    predict_comment_list = []
    # weibo_predict_list = PredictWeiboResult.objects.filter(id__in=weibo_daily_list.values_list('field_id',flat=True))
    for element in weibo_daily_list:
        print(element)
        predict_comment_list.append(element.comment_count_new)
        predict_like_list.append(element.like_count_new)
        predict_forward_list.append(element.forward_count_new)
        date_list.append(str(element.time))
        forward_list.append(element.forward_count)
        like_list.append(element.like_count)
        comment_list.append(element.comment_count)
        # res_dict['日期'] = res_dict['日期'].append(element.time)
        # res_dict['点赞数'] = res_dict['点赞数'].append(element.like_count)
        # res_dict['转发数'] = res_dict['转发数'].append(element.forward_count)
        # res_dict['评论数'] = res_dict['评论数'].append(element.comment_count)

    # weibo_res_dict['predict_date'] = list(weibo_predict_list.values_list('created_at',flat=True))
    weibo_res_dict['predict_like'] = predict_like_list#list(weibo_predict_list.values_list('like_num',flat=True))
    weibo_res_dict['predict_comment'] = predict_comment_list
    weibo_res_dict['predict_forward'] = predict_forward_list
    weibo_res_dict['date'] = date_list
    weibo_res_dict['like'] = like_list
    weibo_res_dict['forward'] = forward_list
    weibo_res_dict['comment'] = comment_list

    #0510修改 预测影响因素
    like_factor = [(0.3152, 'user_mean_of_like'), (0.0602, 'lda_feature2'), (0.0599, 'lda_feature1'), (0.0449, 'blog_60day_avg_weibo'), (0.0437, 'lda_feature0'), (0.0393, 'lda_feature4'), (0.0369, 'blog_60day_sum_weibo'), (0.0317, 'lda_feature3'), (0.0301, 'blog_30day_avg_weibo'), (0.0274, 'content_length'), (0.0248, 'http_number'), (0.0229, 'blog_60day_sum_days'), (0.0226, 'blog_1day_sum_weibo'), (0.0216, 'blog_30day_sum_weibo'), (0.017, 'blog_15day_sum_weibo'), (0.0166, 'weekday'), (0.0152, 'is_have_dianzan'), (0.0151, 'blog_15day_avg_weibo'), (0.0148, 'hour'), (0.0137, 'blog_7day_sum_weibo'), (0.0134, 'blog_3day_sum_weibo'), (0.0131, 'blog_30day_sum_days'), (0.0109, 'blog_7day_avg_weibo'), (0.0108, 'user_percent_forward'), (0.0105, 'user_mean_of_comment'), (0.0102, 'blog_15day_sum_days'), (0.0078, 'user_max_like'), (0.0073, 'user_percent_level4_weibo'), (0.0068, 'user_level1_weibo'), (0.0066, 'at_number'), (0.0054, 'user_percent_level3_weibo'), (0.0036, 'blog_7day_sum_days'), (0.0033, 'user_sum_weibo'), (0.0028, 'weibo_topic_number'), (0.0024, 'user_sum_like'), (0.0021, 'is_have_emoji'), (0.0013, 'user_percent_level5_weibo'), (0.0012, 'user_sum_comment'), (0.0011, 'is_have_zhuanfa'), (0.0009, 'user_percent_zero_interact'), (0.0009, 'user_max_forward'), (0.0007, 'user_percent_level2_weibo'), (0.0006, 'user_mean_of_forward'), (0.0005, 'user_max_interact'), (0.0004, 'user_avg_interact'), (0.0002, 'user_zero_interact'), (0.0002, 'user_percent_like'), (0.0002, 'user_percent_level1_weibo'), (0.0002, 'user_percent_comment'), (0.0002, 'blog_weekend_percent_weibo'), (0.0001, 'user_sum_forward'), (0.0001, 'user_max_comment'), (0.0001, 'user_level5_weibo'), (0.0001, 'user_level4_weibo'), (0.0001, 'user_level3_weibo'), (0.0001, 'user_level2_weibo'), (0.0001, 'blog_week2_percent_weibo'), (0.0, 'user_sum_interact'), (0.0, 'user_min_like'), (0.0, 'user_min_interact'), (0.0, 'user_min_forward'), (0.0, 'user_min_comment'), (0.0, 'blog_weekend_sum_weibo'), (0.0, 'blog_week5_sum_weibo'), (0.0, 'blog_week5_percent_weibo'), (0.0, 'blog_week4_sum_weibo'), (0.0, 'blog_week4_percent_weibo'), (0.0, 'blog_week3_sum_weibo'), (0.0, 'blog_week3_percent_weibo'), (0.0, 'blog_week2_sum_weibo'), (0.0, 'blog_week1_sum_weibo'), (0.0, 'blog_week1_percent_weibo'), (0.0, 'blog_9-17hour_sum_weibo'), (0.0, 'blog_9-17hour_percent_weibo'), (0.0, 'blog_18-0hour_sum_weibo'), (0.0, 'blog_18-0hour_percent_weibo'), (0.0, 'blog_1-8hour_sum_weibo'), (0.0, 'blog_1-8hour_percent_weibo')]
    comment_factor = [(0.1211, 'user_mean_of_comment'), (0.1124, 'lda_feature0'), (0.1111, 'lda_feature1'), (0.0797, 'lda_feature2'), (0.059, 'blog_60day_avg_weibo'), (0.0578, 'is_have_dianzan'), (0.0433, 'lda_feature4'), (0.0402, 'blog_30day_avg_weibo'), (0.0364, 'lda_feature3'), (0.0313, 'content_length'), (0.0259, 'blog_3day_sum_weibo'), (0.0201, 'is_have_zhuanfa'), (0.0199, 'blog_1day_sum_weibo'), (0.0185, 'blog_15day_avg_weibo'), (0.0183, 'blog_30day_sum_weibo'), (0.0181, 'weibo_topic_number'), (0.0179, 'blog_60day_sum_weibo'), (0.0163, 'blog_7day_avg_weibo'), (0.0152, 'blog_30day_sum_days'), (0.0113, 'user_max_like'), (0.0113, 'blog_7day_sum_weibo'), (0.0106, 'hour'), (0.0105, 'user_max_comment'), (0.0101, 'blog_15day_sum_days'), (0.01, 'blog_60day_sum_days'), (0.0088, 'user_percent_level1_weibo'), (0.0076, 'http_number'), (0.0075, 'blog_15day_sum_weibo'), (0.0071, 'weekday'), (0.0051, 'user_percent_level5_weibo'), (0.0045, 'blog_7day_sum_days'), (0.0042, 'at_number'), (0.0025, 'user_percent_like'), (0.0024, 'user_level1_weibo'), (0.002, 'user_sum_interact'), (0.0019, 'user_sum_like'), (0.0018, 'user_mean_of_like'), (0.0017, 'user_level2_weibo'), (0.0017, 'blog_weekend_percent_weibo'), (0.0016, 'user_percent_level2_weibo'), (0.0014, 'user_percent_forward'), (0.0013, 'blog_9-17hour_percent_weibo'), (0.0012, 'user_sum_forward'), (0.0009, 'user_percent_level4_weibo'), (0.0009, 'user_percent_comment'), (0.0009, 'user_level3_weibo'), (0.0008, 'user_percent_zero_interact'), (0.0007, 'user_max_forward'), (0.0007, 'user_level4_weibo'), (0.0007, 'is_have_emoji'), (0.0006, 'user_max_interact'), (0.0006, 'user_avg_interact'), (0.0005, 'user_percent_level3_weibo'), (0.0005, 'blog_week3_percent_weibo'), (0.0003, 'user_zero_interact'), (0.0002, 'user_mean_of_forward'), (0.0002, 'user_level5_weibo'), (0.0002, 'blog_week1_percent_weibo'), (0.0001, 'user_sum_weibo'), (0.0001, 'user_sum_comment'), (0.0001, 'blog_week4_percent_weibo'), (0.0001, 'blog_week2_percent_weibo'), (0.0001, 'blog_18-0hour_percent_weibo'), (0.0, 'user_min_like'), (0.0, 'user_min_interact'), (0.0, 'user_min_forward'), (0.0, 'user_min_comment'), (0.0, 'blog_weekend_sum_weibo'), (0.0, 'blog_week5_sum_weibo'), (0.0, 'blog_week5_percent_weibo'), (0.0, 'blog_week4_sum_weibo'), (0.0, 'blog_week3_sum_weibo'), (0.0, 'blog_week2_sum_weibo'), (0.0, 'blog_week1_sum_weibo'), (0.0, 'blog_9-17hour_sum_weibo'), (0.0, 'blog_18-0hour_sum_weibo'), (0.0, 'blog_1-8hour_sum_weibo'), (0.0, 'blog_1-8hour_percent_weibo')]
    repost_factor = [(0.1144, 'user_mean_of_forward'), (0.0727, 'content_length'), (0.0541, 'is_have_zhuanfa'), (0.0484, 'lda_feature2'), (0.0483, 'lda_feature0'), (0.0457, 'lda_feature4'), (0.0396, 'blog_60day_avg_weibo'), (0.0388, 'lda_feature3'), (0.0387, 'blog_60day_sum_weibo'), (0.0361, 'lda_feature1'), (0.0316, 'blog_7day_avg_weibo'), (0.0309, 'blog_30day_sum_weibo'), (0.0291, 'blog_15day_avg_weibo'), (0.0278, 'blog_7day_sum_weibo'), (0.024, 'http_number'), (0.0232, 'blog_3day_sum_weibo'), (0.0216, 'blog_30day_avg_weibo'), (0.0214, 'hour'), (0.0192, 'user_level3_weibo'), (0.0191, 'blog_60day_sum_days'), (0.0178, 'blog_1day_sum_weibo'), (0.017, 'weekday'), (0.0159, 'blog_15day_sum_weibo'), (0.0152, 'at_number'), (0.0146, 'user_avg_interact'), (0.0145, 'user_sum_forward'), (0.0138, 'user_percent_comment'), (0.0136, 'user_level2_weibo'), (0.013, 'weibo_topic_number'), (0.0108, 'blog_15day_sum_days'), (0.0101, 'blog_30day_sum_days'), (0.0084, 'user_percent_level3_weibo'), (0.008, 'user_mean_of_comment'), (0.0058, 'blog_7day_sum_days'), (0.0045, 'user_max_interact'), (0.0038, 'user_max_forward'), (0.0027, 'user_percent_level5_weibo'), (0.0025, 'is_have_dianzan'), (0.0021, 'blog_weekend_percent_weibo'), (0.002, 'user_percent_like'), (0.002, 'user_percent_level4_weibo'), (0.0018, 'user_percent_level1_weibo'), (0.0017, 'user_percent_level2_weibo'), (0.0017, 'user_max_comment'), (0.0015, 'user_zero_interact'), (0.0014, 'user_mean_of_like'), (0.0014, 'blog_week4_percent_weibo'), (0.0011, 'user_max_like'), (0.001, 'user_sum_like'), (0.001, 'user_level1_weibo'), (0.0006, 'user_sum_comment'), (0.0006, 'user_percent_forward'), (0.0005, 'user_sum_interact'), (0.0005, 'is_have_emoji'), (0.0004, 'user_percent_zero_interact'), (0.0004, 'blog_9-17hour_percent_weibo'), (0.0003, 'blog_week1_percent_weibo'), (0.0003, 'blog_18-0hour_percent_weibo'), (0.0002, 'user_level5_weibo'), (0.0002, 'user_level4_weibo'), (0.0002, 'blog_week2_percent_weibo'), (0.0001, 'user_sum_weibo'), (0.0001, 'blog_week3_percent_weibo'), (0.0, 'user_min_like'), (0.0, 'user_min_interact'), (0.0, 'user_min_forward'), (0.0, 'user_min_comment'), (0.0, 'blog_weekend_sum_weibo'), (0.0, 'blog_week5_sum_weibo'), (0.0, 'blog_week5_percent_weibo'), (0.0, 'blog_week4_sum_weibo'), (0.0, 'blog_week3_sum_weibo'), (0.0, 'blog_week2_sum_weibo'), (0.0, 'blog_week1_sum_weibo'), (0.0, 'blog_9-17hour_sum_weibo'), (0.0, 'blog_18-0hour_sum_weibo'), (0.0, 'blog_1-8hour_sum_weibo'), (0.0, 'blog_1-8hour_percent_weibo')]
    #0522 修改 图表显示关系
    from django.db.models import Min, Avg, Max, Sum
    factor_info = WeiboTrainDataFeature.objects.filter().values('blog_15day_sum_days').annotate(
        comment_count=Avg('forward_count')).order_by('blog_15day_sum_days')[:100000]
    factor_list = {}
    # mid_list = []
    # interact_list = []
    # for i in factor_info:
    #     mid_list.append(i.mid)
    #     interact_list.append(i.sum_interact)
    factor_list['comment_count'] = [i[0] for i in factor_info.values_list('comment_count')]
    factor_list['blog_15day_sum_days'] = [i[0] for i in factor_info.values_list('blog_15day_sum_days')]
    return render(request, 'index/tianchi_blogger_visual.html',{'factor_list':factor_list,'weibo_analyse_list':weibo_res_dict,'like_factor':like_factor,'comment_factor':comment_factor,'repost_factor':repost_factor})#'user_info':user_info


def handleSearch(request):
    ret = {'status': True, 'error': ""}
    try:
        search_id = request.POST.get('search_id')
        search_type = request.POST.get('search_type')
        if search_type == '查看微博数据':
            res = Weibo.objects.filter(field_id = search_id)
            if(len(res) == 0):
                ret['status'] = False
                ret['error'] = '该条微博不存在，请重试！'
        elif search_type == '查看博主数据' or search_type == '查看博主主页':
            res = Information.objects.filter(field_id = search_id)
            if(len(res) == 0):
                ret['status'] = False
                ret['error'] = '博主ID不存在，请重试！'
        elif search_type == '查看博主数据(天池)':
            pass

    except Exception as e:
        ret['status'] = False
        ret['error'] = str(e)
    j_ret = json.dumps(ret)
    return HttpResponse(j_ret)


def handleShowFactorDialog(request):
    ret = {'status': True, 'error': ""}
    try:
        factor_name = request.POST.get('factor_name')
        y_name = request.POST.get('y_name')
        from django.db.models import Min, Avg, Max, Sum
        factor_info = WeiboTrainDataFeature.objects.filter().values(factor_name).annotate(
            count=Avg(y_name)).order_by(factor_name).values('count',factor_name)[:100000]
        factor_list = {}
        factor_list[y_name] = [i[0] for i in factor_info.values_list('count')]
        factor_list[factor_name] = [i[0] for i in factor_info.values_list(factor_name)]
        ret['data'] = factor_list
    except Exception as e:
        ret['status'] = False
        ret['error'] = str(e)
    j_ret = json.dumps(ret)
    return HttpResponse(j_ret)



def index(request):
    weibo = Weibo.objects.all().order_by('-created_at')  # user_id
    blogger_info = Information.objects.filter(is_blogger = 1).order_by('-crawl_time')
    for element in weibo:
        weibo_id = element.field_id
        weibo_key_word = TrainKeyWordTextRank.objects.filter(weibo_id = weibo_id)
        if(len(weibo_key_word) > 0):
            element.key_word = weibo_key_word[0].word
            element.key_weight = weibo_key_word[0].weight
        else:
            element.key_word = ''
            element.key_weight = ''
        weibo_sentiment_info = SentimentWeiboResult051802.objects.filter(mid = weibo_id)
        if (len(weibo_sentiment_info) > 0):
            element.is_positive = weibo_sentiment_info[0].is_positive
            element.sentiment_score = [float(i) for i in weibo_sentiment_info[0].sentiment_score.split(',')]
        else:
            element.is_positive = ''
            element.sentiment_score = ''

    # return HttpResponse(information.fans_num)
    # weibo_info = weibo[:30]
    # try:
    #     for element in weibo_info:
    #         #外键好像直接会把外检变为对象
    #         element.nick_name = element.user.nick_name
    #         element.portrait = element.user.portrait
    #         # element.sex = element.user.gender
    #         # element.brief_introduction = element.user.brief_introduction
    #         pic_url = element.pic_url.split(',')
    #         last_pic_url = element.last_pic_url.split(',')
    #         element.pic_url = []
    #         if pic_url != ['']:
    #             element.pic_url = element.pic_url + pic_url
    #             if last_pic_url != ['']:
    #                 element.pic_url = element.pic_url + last_pic_url
    #         if last_pic_url != ['']:
    #             element.pic_url = element.pic_url + last_pic_url
    # except Exception as e:
    #     print(e)
    try:
        paginator = Paginator(weibo, 10)
        try:
            page_number = request.GET.get('page', '1')
            page = paginator.page(page_number)
        except (PageNotAnInteger, EmptyPage, InvalidPage):
            # 如果出现上述异常，默认展示第1页
            page = paginator.page(1)
        for element in page.object_list:
            element.nick_name = element.user.nick_name
            element.portrait = element.user.portrait
            pic_url = element.pic_url.split(',')
            last_pic_url = element.last_pic_url.split(',')
            element.pic_url = []
            if pic_url != ['']:
                element.pic_url = element.pic_url + pic_url
                if last_pic_url != ['']:
                    element.pic_url = element.pic_url + last_pic_url
            if last_pic_url != ['']:
                element.pic_url = element.pic_url + last_pic_url

    except Exception as e:
        print(e)
    # element.pic_url = ['http://wx2.sinaimg.cn/wap180/006dWiXzly1fpde9eihxyj31kw1kwkjl.jpg']
    return render(request, 'index/index2.html', {'user_info': blogger_info,'page':page })#'user_weibo': weibo_info


def factorVisual(request):
    import pandas as pd
    from django.db.models import Min, Avg, Max, Sum
    factor_info = WeiboTrainDataFeature.objects.filter().values('blog_15day_sum_days').annotate(comment_count = Avg('forward_count')).order_by('blog_15day_sum_days')[:100000]
    factor_list = {}
    # mid_list = []
    # interact_list = []
    # for i in factor_info:
    #     mid_list.append(i.mid)
    #     interact_list.append(i.sum_interact)
    factor_list['comment_count'] = [ i[0] for i in factor_info.values_list('comment_count')]
    factor_list['blog_15day_sum_days'] = [ i[0] for i in factor_info.values_list('blog_15day_sum_days')]
    return render(request, 'index/factor_visual.html',{'factor_list':factor_list})#'user_info':user_info


def getBloggerOption(request):#待区分用户
    ret = {'status': True, 'error': ""}
    try:
        blogger_list = Information.objects.filter(is_blogger = 1).values('field_id','nick_name')
        ret['data'] = list(blogger_list)
    except Exception as e:
        ret['status'] = False
        ret['error'] = str(e)
    j_ret = json.dumps(ret)
    return HttpResponse(j_ret)


def getTianchiBloggerOption(request):
    ret = {'status': True, 'error': ""}
    try:
        blogger_list = PredictWeiboResult2.objects.all().values('uid').annotate(total_records = Count('mid')).order_by('-total_records')
        print(blogger_list)
        ret['data'] = list(blogger_list)
    except Exception as e:
        ret['status'] = False
        ret['error'] = str(e)
    j_ret = json.dumps(ret)
    return HttpResponse(j_ret)



def getWeiboOption(request):#待区分用户
    ret = {'status': True, 'error': ""}
    try:
        weibo_id_list = Weibo.objects.all().order_by('-crawl_time').values('field_id')
        # weibo_id_list = Weibo.objects.all().values('user').annotate(total_records = Count('field_id')).order_by('-total_records').values('field_id')
        ret['data'] = list(weibo_id_list)
    except Exception as e:
        ret['status'] = False
        ret['error'] = str(e)
    j_ret = json.dumps(ret)
    return HttpResponse(j_ret)
