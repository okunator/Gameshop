from django.shortcuts import render
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy, reverse
from . import forms
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.conf import settings
User = settings.AUTH_USER_MODEL

class SignUp(UserPassesTestMixin, generic.CreateView):
    form_class = forms.UserCreateForm           # SignUp-form is an instance of UserCreateForm-class from forms.py
    success_url = reverse_lazy('login')         # After signup, redirection to login-page
    template_name = 'accounts/signup.html'
    raise_exception = True

    def test_func(self):
        if self.request.user.is_authenticated:
            False
        else:
            return True

class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    form_class = forms.UserUpdateForm
    template_name = 'accounts/user_update_form.html'
    success_message = "%(username)s's info has been updated"

    def get_success_url(self):
        return reverse('home')

    #get object
    def get_object(self, queryset=None):
        return self.request.user

    #override form_valid method
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)
