from django.conf.urls import url
from django.contrib.auth import views as auth_views #built-in login and logout passwordchange view and what-not
from . import views
from django.core.urlresolvers import reverse_lazy


# TEMPLATE TAG
app_name = 'accounts'

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url(r'^update/(?P<username>[\w\-]+)/$', views.UserUpdateView.as_view(), name='profile_update'),

    url(r'^password_reset/$',
        auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html',
        success_url=reverse_lazy('accounts:password_reset_done'),
        subject_template_name='accounts/password_reset_subject.txt'),
        name='password_reset'),

    url(r'^password_reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),

    url(r'^reset/<uidb64>/<token>/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'),

    url(r'^reset/done/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),
]
