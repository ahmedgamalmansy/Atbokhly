from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from idlelib.configDialog import is_int
from difflib import SequenceMatcher
from user_profile.models import *

from django.forms import ModelForm


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



def validate_username(value):
    qs = User.objects.filter(username=value)
    if qs.exists():
        raise forms.ValidationError("اسم المستخدم مسجل لدينا برجاء اختيار اسم اخر او اعادة ضبط كلمة السر الخاصة بك")

class LoginForm(forms.Form):
    user_name = forms.CharField(required=True,widget=forms.TextInput(
        attrs={
                "class" :"form-control",
                "placeholder" :"اسم المستخدم"

        }
    ))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            "placeholder": "كلمة المرور"

        }
    ))



class email_update_form(forms.Form):
    email = forms.CharField(required=True, widget=forms.TextInput(
        attrs={

            "placeholder": "البريد الإلكترونى الجديد",
            "type": "email"
        }
    ))


class respond_request(ModelForm):
    class Meta:
        model = ChiefProfile
        fields = ['state']
