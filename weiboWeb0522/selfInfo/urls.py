from django.conf.urls import url

from . import views
from django.urls import reverse
#0522修改 上传头像
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
app_name = 'self'
urlpatterns = [
    url(r'^$', views.selfInfo, name='selfInfo'),
    url(r'^addObserver/$', views.addObserver, name='addObserver'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^toLogin/$', views.toLogin, name='toLogin'),
    url(r'^selfCenter/$', views.selfCenter, name='selfCenter'),
    url(r'^updateToDB/$', views.updateToDB, name='updateToDB'),
    url(r'^registerToDB/$', views.registerToDB, name='registerToDB'),
    url(r'^deleteObserver/(?P<id>[0-9]+)/$', views.deleteObserver, name='deleteObserver'),
    url(r'^getFrequencyList/$', views.getFrequencyList, name='getFrequencyList'),
    url(r'^updateFrequency/$', views.updateFrequency, name='updateFrequency'),
    #0522修改 上传头像
    url(r'^uploadImg/$', views.uploadImg,name='uploadImg'), # 新增
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),

]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
              #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)