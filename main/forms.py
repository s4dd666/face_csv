from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class GenerateUsersForm(forms.Form):
    num_users = forms.IntegerField(min_value=1, max_value=1000)

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))

