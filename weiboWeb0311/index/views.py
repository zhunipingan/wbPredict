from django.shortcuts import render
from django.db.models import Sum
# Create your views here.
from django.http import HttpResponse
# from .models import TrainData
import datetime
from .models import Weibo
from .models import Information

def index(request):
    weibo = Weibo.objects.all().order_by('created_time')
    weibo_list = weibo.values('created_date').annotate(like = Sum('like_num'),forward = Sum('repost_num'), comment= Sum('comment_num')).values('created_date','like','forward','comment').order_by('created_date')
    weibo_pie = Weibo.objects.all().aggregate(like = Sum('like_num'),forward = Sum('repost_num'), comment= Sum('comment_num'))#.values('like','forward','comment')
    # return HttpResponse(weibo_pie)
    res_dict = {}
    # res_dict = {'日期': list, '点赞数': list, '转发数' :list,'评论数':list}
    date_list = []
    forward_list = []
    like_list = []
    comment_list = []
    for element in weibo_list:
        date_list.append(element['created_date'])
        forward_list.append(element['forward'])
        like_list.append(element['like'])
        comment_list.append(element['comment'])
        # res_dict['日期'] = res_dict['日期'].append(element.time)
        # res_dict['点赞数'] = res_dict['点赞数'].append(element.like_count)
        # res_dict['转发数'] = res_dict['转发数'].append(element.forward_count)
        # res_dict['评论数'] = res_dict['评论数'].append(element.comment_count)

    # return HttpResponse("欢迎访问我的博客首页！")
    res_dict['date'] = date_list
    res_dict['like'] = like_list
    res_dict['forward'] = forward_list
    res_dict['comment'] = comment_list

    pie_info = {
        'like':weibo_pie['like'],
        'forward':weibo_pie['forward'],
        'comment':weibo_pie['comment']
    }

    information = Information.objects.get(field_id = '5659628156')
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
            'labels':information.labels
        }
    else:
        user_info = {
            'name': 'ERROR',
            'introduction': 'ERROR',
            'fans': 0,
            'follows': 0,
            'blogs': 0
        }
    return render(request, 'index/index2.html',{'list':res_dict,'pie':pie_info,'user_info':user_info})

