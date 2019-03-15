from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from .models import Observer,User
import json
import time
from index.models import Information

def selfInfo(request):

    observe_list = Observer.objects.all().order_by('-add_time')
    for element in observe_list:
        if element.crawl_time is None:
            element.crawl_time = '--'
        try:
            # return HttpResponse(Information.objects.get(field_id = userId))
            element.nick_name = Information.objects.get(field_id = element.user_id).nick_name
        except:
            element.nick_name = '--'
    return render(request, 'selfInfo/selfInfo.html', context={
                      'observe_list': observe_list
                  })



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
