from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from .models import Observer,MyUser
import json
import time
from index.models import Information
import datetime

def selfInfo(request):
    #已有是否登录认证
    my_phone = request.session.get('my_phone', default=None)
    if my_phone is not None:
        observe_list = Observer.objects.all().order_by('-add_time')

        for element in observe_list:
            if element.crawl_time is None:
                element.crawl_time = '--'
            try:
                # return HttpResponse(Information.objects.get(field_id = userId))
                element.nick_name = Information.objects.get(field_id = element.user_id).nick_name
            except:
                element.nick_name = '--'
        return render(request, 'selfInfo/self_info2.html', context={
                          'observe_list': observe_list
                      })
    else:
        return redirect('/self/login')



def addObserver(request):
    ret = {'status': True, 'error': ""}
    try:
        user_id = request.POST.get('user_id')
        res = Observer.objects.filter(user_id = user_id).count()
        if res > 0:
            ret['status'] = False
            ret['error'] = '新增失败，该用户处于被观测序列中！'
        else:
            observer = Observer()
            observer.user_id = user_id
            observer.add_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            observer.crawl_count = 0
            observer.is_exist = 0
            observer.save()
            print('添加新博主成功')

    except Exception as e:
        ret['status'] = False
        ret['error'] = str(e)
    j_ret = json.dumps(ret)
    return HttpResponse(j_ret)


def deleteObserver(request,id):
    Observer.objects.filter(id=id).delete()
    return redirect("/self/")


def register(request):
    return render(request,'selfInfo/register.html')

def registerToDB(request):
    ret = {'status': True, 'error': ""}
    try:
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        nick_name = request.POST.get('nick_name')

        print('registerToDB',name)
        res = MyUser.objects.filter(phone = phone).count()
        if res > 0:
            ret['status'] = False
            ret['error'] = '新增失败，该手机号码已注册！'
        else:
            myUser = MyUser()
            myUser.nick_name = nick_name
            myUser.name = name
            myUser.password = password
            myUser.phone = phone
            myUser.register_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            myUser.save()
    except Exception as e:
        ret['status'] = False
        ret['error'] = str(e)
    j_ret = json.dumps(ret)
    return HttpResponse(j_ret)


def login(request):
    return render(request,'selfInfo/login.html')

def selfCenter(request):
    # 已有是否登录认证
    my_phone = request.session.get('my_phone', default=None)
    if my_phone is not None:
        my_info = MyUser.objects.get(phone = my_phone)
        return render(request, 'selfInfo/self_center.html',{'my_info':my_info})
    else:
        return redirect('/self/login')


def updateToDB(request):
    ret = {'status': True, 'error': ""}
    try:
        phone = request.session.get('my_phone', default=None)
        name = request.POST.get('name')
        nick_name = request.POST.get('nick_name')
        res = MyUser.objects.filter(phone = phone).count()
        if res == 0:
            ret['status'] = False
            ret['error'] = '更新失败，该用户未注册！'
        else:
            MyUser.objects.filter(phone = phone).update(name = name,nick_name = nick_name)
            ret['status'] = True
            ret['error'] = '更新成功！'
    except Exception as e:
        ret['status'] = False
        ret['error'] = str(e)
    j_ret = json.dumps(ret)
    return HttpResponse(j_ret)



def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/self")
    request.session.flush()
    return redirect("/self")


def toLogin(request):
    ret = {'status': False, 'error': "密码错误！"}
    try:
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        res = MyUser.objects.get(phone = phone)
        if res.password == password:
            request.session['my_phone'] = phone
            request.session['is_login'] = True
            ret['status'] = True
            ret['error'] = ''
    except Exception as e:
        ret['status'] = False
        ret['error'] = '登录失败，该手机号码未注册！'
    j_ret = json.dumps(ret)
    return HttpResponse(j_ret)



# from django.db import models
# from django.urls import reverse
#
# class Observer(models.Model):
#     id = models.IntegerField(primary_key=True)
#     user_id = models.CharField(max_length=255, blank=True, null=True)
#     my_id = models.IntegerField(blank=True, null=True)
#     add_time = models.DateTimeField(blank=True, null=True)
#     crawl_time = models.DateTimeField(blank=True, null=True)
#     crawl_count = models.BigIntegerField(blank=True, null=True)
#     is_exist = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         db_table = 'observer'
#
#     def get_absolute_url(self):
#         return reverse('self:deleteObserver', kwargs={'id': self.id})
#
#     def get_absolute_url2(self):
#         return reverse('index:userInfo', kwargs={'userId': self.user_id})
#
#
# class User(models.Model):
#     id = models.IntegerField(primary_key=True)
#     register_time = models.DateTimeField(blank=True, null=True)
#     name = models.CharField(max_length=255, blank=True, null=True)
#     password = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         db_table = 'user'


