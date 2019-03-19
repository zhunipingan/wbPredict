from django.shortcuts import render,redirect
from django.db.models import Sum
# Create your views here.
from django.http import HttpResponse
# from .models import TrainData
import datetime
from .models import Weibo
from .models import Information
from .models import WeiboDailyNum
from .models import UserDailyNum,Relationship,Comment
from django.db.models.aggregates import Count
import numpy as np

from django.db.models import F,Q
from django.db.models.functions.datetime import TruncMonth,TruncYear
import jieba
import codecs
import collections # 词频统计库
import json

def weiboVisual(request,weiboId):
    userId = weiboId.split('_')[0]
    #博主的微博list
    weibo_list = Weibo.objects.filter(Q(user = userId) & ~Q(field_id = weiboId)).order_by('-created_at')

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

    weibo_pie = weibo_daily_list.first()
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
        print('like_num',weibo_pie.like_num/pie_sum,pie_sum)
        pie_info2 = [{'name':'点赞数','value':weibo_pie.like_num,'percent':round(weibo_pie.like_num/pie_sum*100,2)},{'name':'转发数','value':weibo_pie.repost_num,
        'percent':round(weibo_pie.repost_num/pie_sum*100,2)},{'name':'评论数','value':weibo_pie.comment_num,'percent':round(weibo_pie.comment_num/pie_sum*100,2)}]
        pie_info = {
            'like':weibo_pie.like_num,
            'forward':weibo_pie.repost_num,
            'comment':weibo_pie.comment_num#weibo_pie['comment']
        }

    # 评论信息1699432410_HkZIvDKo3
    comment_info_list = Comment.objects.filter(weibo_url='1699432410_HkZIvDKo3')
    hot_comment = comment_info_list[:5]
    stop_words_txt = codecs.open(r'D:\graduation project\weiboWeb\extraFile\GlobalStopWords.txt', 'r', encoding='UTF-8').readlines()
    stop_words = [word.strip('\n') for word in stop_words_txt]
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


        # element.pic_url = ['http://wx2.sinaimg.cn/wap180/006dWiXzly1fpde9eihxyj31kw1kwkjl.jpg']
    return render(request, 'index/weibo_visual3.html',{'list':res_dict,'pie':pie_info,'pie2':pie_info2,'word_cloud':word_cloud_list,'user_info':information,'hot_comment':hot_comment,'weibo_list':weibo_list})#'user_info':user_info


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

    weibo_info = weibo[:10]
    for element in weibo_info:
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
    return render(request, 'index/user_info2.html',{'user_info':user_info,'user_weibo':weibo_info})


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
    #年龄分布
    now_year = datetime.datetime.now().year
    age_group = fans_info_list.filter(birthday__regex="^\d{4}-\d{1,2}-\d{1,2}").annotate(date = TruncYear('birthday')).values('date')#.annotate(values = Count('field_id'))
    age_list = [(now_year - age['date'].year)//10 for age in age_group ]
    age_info = []
    age_name_info = []
    for i in set(age_list):
        age_dict = {}
        age_dict['name'] = str(i*10)+'-'+str(i*10+9)+'岁'
        age_name_info.append(age_dict['name'])
        age_dict['value'] = age_list.count(i)
        age_info.append(age_dict)

    return render(request, 'index/blogger_visual2.html',{'list':res_dict,'sex_info':sex_info,'location_info':location_list,'foreign_fans_num':len(location_group)-len(location_list),'age_info':age_info,'user_info':information})#'user_info':user_info


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
    except Exception as e:
        ret['status'] = False
        ret['error'] = str(e)
    j_ret = json.dumps(ret)
    return HttpResponse(j_ret)


def index(request):
    weibo = Weibo.objects.all().order_by('-created_at')  # user_id
    blogger_info = Information.objects.filter(is_blogger = 1).order_by('-crawl_time')
    # return HttpResponse(information.fans_num)
    weibo_info = weibo[:30]
    try:
        for element in weibo_info:
            #外键好像直接会把外检变为对象
            element.nick_name = element.user.nick_name
            element.portrait = element.user.portrait
            # element.sex = element.user.gender
            # element.brief_introduction = element.user.brief_introduction
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
    return render(request, 'index/index2.html', {'user_info': blogger_info, 'user_weibo': weibo_info})


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


def getWeiboOption(request):#待区分用户
    ret = {'status': True, 'error': ""}
    try:
        weibo_id_list = Weibo.objects.all().values('field_id')
        ret['data'] = list(weibo_id_list)
    except Exception as e:
        ret['status'] = False
        ret['error'] = str(e)
    j_ret = json.dumps(ret)
    return HttpResponse(j_ret)
