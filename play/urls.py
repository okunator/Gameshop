from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


# TEMPLATE TAG
app_name = 'play'

urlpatterns = [
    url(r'^$', views.PlayTemplateView.as_view(), name='play'),
    url(r'^game/(?P<slug>[\w\-]+)/$', views.PlayDetailView.as_view(), name='playdetail'),
]
