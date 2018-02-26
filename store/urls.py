from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'store'

urlpatterns = [
    url(r'^add/$', views.AddGame.as_view(), name='addgame'),
    url(r'^game/(?P<slug>[\w\-]+)/$',views.GameDetailView.as_view(), name='gamedetail'),
    url(r'^delete/(?P<slug>[\w\-]+)/$', views.GameDeleteView.as_view(), name='delete'),
    url(r'^buy/(?P<slug>[\w\-]+)/$', views.BuyView.as_view(), name='buy'),
    url(r'^buy/paymentsuccess/*', views.PaymentSuccessTemplateView.as_view(), name='pay_success'),
    url(r'^buy/paymentstopped/*', views.PaymentCancelTemplateView.as_view(), name='pay_cancel'),
    url(r'^update/(?P<slug>[\w\-]+)/$', views.GameUpdateView.as_view(), name='update'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.ProfileListView.as_view(), name='profile'),

    url(r'^password_change/$',
        auth_views.PasswordChangeView.as_view(template_name='store/password_change_form.html'),
        name='password_change'),

    url(r'^password_change/done/$',
       auth_views.PasswordChangeDoneView.as_view(template_name='store/password_change_done.html'),
       name='password_change_done'),
]
