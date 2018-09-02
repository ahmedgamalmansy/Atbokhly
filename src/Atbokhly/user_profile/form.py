from django import forms
from django.forms import ModelForm
from .models import UserProfile , ChiefProfile


class UpdateChiefProfileForm(ModelForm):
    class Meta:
        model = ChiefProfile
        fields = '__all__'

class UpdateUserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        # "birth_date".widgets = forms.DateField(attrs={"type": "date"})
class email_update_form(forms.Form):
    email = forms.CharField(required=True, widget=forms.TextInput(
        attrs={

            "placeholder": "البريد الإلكترونى الجديد",
            "type": "email"
        }
    ))