from django.conf.urls import url

from . import views
app_name = 'index'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^u/(?P<userId>.*)/$', views.userInfo, name='userInfo'),
    url(r'^factorVisual/$', views.factorVisual, name='factorVisual'),
    url(r'^blogger/(?P<bloggerId>.*)/$', views.bloggerVisual, name='bloggerVisual'),
    url(r'^bloggerTianchi/(?P<bloggerId>.*)/$', views.bloggerTianchiVisual, name='bloggerTianchiVisual'),
    url(r'^weibo/(?P<weiboId>.*)/$', views.weiboVisual, name='weiboVisual'),
    url(r'^handleSearch/$', views.handleSearch, name='handleSearch'),
    url(r'^handleShowFactorDialog/$', views.handleShowFactorDialog, name='handleShowFactorDialog'),
    url(r'^getBloggerOption/$', views.getBloggerOption, name='getBloggerOption'),
    url(r'^getTianchiBloggerOption/$', views.getTianchiBloggerOption, name='getTianchiBloggerOption'),
    url(r'^getWeiboOption/$', views.getWeiboOption, name='getWeiboOption'),
]