from django.conf.urls import url

from . import views
from django.urls import reverse
app_name = 'self'
urlpatterns = [
    url(r'^$', views.selfInfo, name='selfInfo'),
    url(r'^addObserver/$', views.addObserver, name='addObserver'),
    url(r'^deleteObserver/(?P<id>[0-9]+)/$', views.deleteObserver, name='deleteObserver'),
]