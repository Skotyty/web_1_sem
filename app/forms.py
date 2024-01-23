from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ImageField

from app.models import Question


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)

    def clean_password(self):
        data = self.cleaned_data['password']
        if data == 'wrongpass':
            raise ValidationError('Wrong password')
        return data


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class SettingsForm(forms.ModelForm):
    avatar = ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def save(self, **kwargs):
        user = super().save(**kwargs)

        profile = user.profile
        received_avatar = self.cleaned_data.get('avatar')
        if received_avatar:
            profile.avatar = received_avatar
            profile.save()

        return user


class QuestionForm(forms.ModelForm):
    tags = forms.CharField(required=False)

    class Meta:
        model = Question
        fields = ['title', 'text']
