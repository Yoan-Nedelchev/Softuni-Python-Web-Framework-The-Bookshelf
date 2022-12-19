from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from theBookshelf.accounts.models import Profile
from theBookshelf.common.models import News

UserModel = get_user_model()


class CreateNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('header', 'title', 'content')
