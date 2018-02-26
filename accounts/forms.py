from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm # built-in user-creation form

class UserCreateForm(UserCreationForm):
    class Meta():
        fields = ('username', 'email', 'is_developer', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = 'Username'
        self.fields['email'].label = 'Email'
        self.fields['is_developer'].label = 'Developer'


class UserUpdateForm(forms.ModelForm):
    class Meta:
        fields = ['username', 'email', 'is_developer']
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = 'Username'
        self.fields['email'].label = 'Email'
        self.fields['is_developer'].label = 'Developer'
