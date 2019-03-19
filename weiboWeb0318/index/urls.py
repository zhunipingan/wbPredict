from django.conf.urls import url

from . import views
app_name = 'index'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^u/(?P<userId>.*)/$', views.userInfo, name='userInfo'),
    url(r'^blogger/(?P<bloggerId>.*)/$', views.bloggerVisual, name='bloggerVisual'),
    url(r'^weibo/(?P<weiboId>.*)/$', views.weiboVisual, name='weiboVisual'),
    url(r'^handleSearch/$', views.handleSearch, name='handleSearch'),
    url(r'^getBloggerOption/$', views.getBloggerOption, name='getBloggerOption'),
    url(r'^getWeiboOption/$', views.getWeiboOption, name='getWeiboOption'),
]