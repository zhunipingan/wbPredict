from django.shortcuts import render
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

from django.db.models import F

def weiboVisual(request,weiboId):
    userId = weiboId.split('_')[0]
    weibo_list = WeiboDailyNum.objects.filter(weibo = weiboId).order_by('crawl_time')
    # weibo_pie = weibo_list.aggregate(like = Sum('like_num'),forward = Sum('repost_num'), comment= Sum('comment_num'))#.values('like','forward','comment')
    res_dict = {}
    # res_dict = {'日期': list, '点赞数': list, '转发数' :list,'评论数':list}
    date_list = []
    forward_list = []
    like_list = []
    comment_list = []
    for element in weibo_list:
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

    weibo_pie = weibo_list.first()
    if weibo_pie is None:
        pie_info = {
            'like': 0,
            'forward': 0,
            'comment': 0  # weibo_pie['comment']
        }
    else:
        pie_info = {
            'like':weibo_pie.like_num,
            'forward':weibo_pie.repost_num,
            'comment':weibo_pie.comment_num#weibo_pie['comment']
        }

    # information = Information.objects.get(field_id = userId)
    # # return HttpResponse(information.fans_num)
    #
    # if information:
    #     if information.city == 'None':
    #         information.city = ''
    #     if information.gender == 'None':
    #         information.gender = '保密'
    #     if information.birthday == 'None':
    #         information.birthday = '保密'
    #     if information.sex_orientation == 'None':
    #         information.sex_orientation = '保密'
    #     if information.labels == 'None':
    #         information.labels = '无'
    #     user_info = {
    #         'name':information.nick_name,
    #         'introduction':information.brief_introduction,
    #         'fans':information.fans_num,
    #         'follows':information.follows_num,
    #         'blogs':information.weibo_num,
    #         'gender':information.gender,
    #         'location':information.province + ' ' + information.city,
    #         'birthday':information.birthday,
    #         'sex_orientation':information.sex_orientation,
    #         'labels':information.labels,
    #         'portrait':information.portrait
    #     }
    # else:
    #     user_info = {
    #         'name': 'ERROR',
    #         'introduction': 'ERROR',
    #         'fans': 0,
    #         'follows': 0,
    #         'blogs': 0
    #     }

    # weibo_info = weibo_list[:10]
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


        # element.pic_url = ['http://wx2.sinaimg.cn/wap180/006dWiXzly1fpde9eihxyj31kw1kwkjl.jpg']
    return render(request, 'index/weibo_visual.html',{'list':res_dict,'pie':pie_info})#'user_info':user_info


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
    return render(request, 'index/user_info.html',{'user_info':user_info,'user_weibo':weibo_info})


def bloggerVisual(request,bloggerId):
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

    pie_info = {
        'like': 0,
        'forward': 0,
        'comment': 0  # weibo_pie['comment']
    }

    fans_id_list = Relationship.objects.filter(followed_id = bloggerId).values('fan_id')
    fans_info_list = Information.objects.filter(field_id__in = fans_id_list)
    location_group = fans_info_list.values('province').annotate(name=F('province'),value = Count('field_id')).values('name','value')
    # print(list(location_group))
    location_list = list(location_group)
    province_list = []
    location_list = [element for element in location_list if element['name'] != '海外']
    sex_group = fans_info_list.values('gender').annotate(value = Count('field_id'))
    sex_info = []
    for element in sex_group:
        sex_dict = dict()
        sex_dict['name'] = element['gender']
        sex_dict['value'] = int(element['value'])
        sex_info.append(sex_dict)

    return render(request, 'index/blogger_visual.html',{'list':res_dict,'pie':pie_info,'sex_info':sex_info,'location_info':list(location_group)})#'user_info':user_info

