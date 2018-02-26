"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.HomePageListView.as_view(), name='home'),
    url(r'^', include('store.urls', namespace='store')),
    url(r'^', include('django.contrib.auth.urls')), #connect built-in authorization
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^accounts/', include('django.contrib.auth.urls')), #connect built-in authorization
    url(r'^test/$', views.TestPage.as_view(), name='test'),
    url(r'^thanks/$', views.ThanksPage.as_view(), name='thanks'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^play/', include('play.urls',namespace='play')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
