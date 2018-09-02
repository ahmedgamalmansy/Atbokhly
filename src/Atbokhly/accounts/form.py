from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from idlelib.configDialog import is_int
from difflib import SequenceMatcher



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
    def clean_user_name(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username)
        if user.exists() and user.is_active:
            raise forms.ValidationError(u'sorry you account got banned not active if you did not activate it please do it through the confirmation mail we sent you')
        return email


class RegisterForm(forms.Form):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'هذا البريد الالكترونى مسجل لدينا برجاء اختيار بريد الكترونى اخر')
        return email
    user_name = forms.CharField(required=True,widget=forms.TextInput(
        attrs={

                "placeholder" :"اسم المستخدم"

        }
    ),validators=[validate_username])
    first_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            "placeholder": "الاسم الاول"
        }
    ))
    last_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={

            "placeholder": "اسم العائلة"

        }
    ))
    email = forms.CharField(required=True, widget=forms.TextInput(
        attrs={

            "placeholder": "البريد الإلكترونى",
            "type": "email"
        }
    ))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={

            "placeholder": "كلمة المرور"

        }
    ))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={

            "placeholder": "تأكيد كلمة المرور"

        }
    ))
    cv = forms.FileField(required=False)
    CHOICES = [('cheif', 'cheif'),
               ('normal_user', 'normal_user')]

    # user_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    user_type = forms.ChoiceField(label="",choices=CHOICES, initial='', widget=forms.RadioSelect(), required=True)

    def clean_password(self):
        password = self.cleaned_data.get("password")
        username = self.cleaned_data.get("user_name")
        if username and SequenceMatcher(None, password, username).ratio() > 0.7:
            raise forms.ValidationError(u'كلمة السر مشابهة جدا لاسم المستخدم')
        elif len(password) < 8 or not (any(x.isdigit() for x in password)) or not(any(x.isupper() for x in password)) or not (any(x.islower() for x in password)):
            raise forms.ValidationError([
                u'كلمة السر يجب ان تتوفر على 8 أحرف على الاقل',
                u'كلمة السر يجب ان تحتوى على رقم واحد على الاقل',
                u'كلمة السر يجب ان تحتوى على حرف صغير lowercase letter على الاقل',
                u'كلمة السر يجب ان تحتوى على حرف كبير uppercase letter على الاقل'
            ])

        return password

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password != password2:
            raise forms.ValidationError('كلمة السر غير متطابقة')

        return password2