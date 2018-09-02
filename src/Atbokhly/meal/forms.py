from idlelib.configDialog import is_int
from django import forms
from .models import Meal,Comment
import os

def validate_feedback(value):
    for i in value:
        if is_int(i) or i in '!@#$%^&*()_+}{][|?/"><;.:=-`~\'\\':
            raise forms.ValidationError(u' هذا الاسم غير صحيح يجب الا يتوفر الاسم ع ارقام او رموز')


class Add_meal(forms.ModelForm):
    def clean_video(self):
        if self.cleaned_data['video']:
            name, ext = str(self.cleaned_data['video']).split(os.extsep)
            if ext.lower() in ['mp4', 'mkv']:
                return self.cleaned_data['video']
            raise forms.ValidationError(u'يجب ان يكون الفيديو بامتداد .MP4 او .MKV')
        return None

    def clean_meal_name(self):
        meal_name = self.cleaned_data['meal_name']
        for i in meal_name:
            if is_int(i) or i in '!@#$%^&*()_+}{][|?/"><.:=;-`~\'\\':
                raise forms.ValidationError(u' هذا الاسم غير صحيح يجب الا يتوفر الاسم ع ارقام او رموز')
        else:
            return meal_name

    class Meta:
        model = Meal
        fields = [
            'meal_name',
            'meal_recipe',
            'meal_category',
            'ingredients',
            'img',
            # 'video'
        ]


class feedbackCreateForm(forms.Form):
    name    = forms.CharField(label="",required=False,widget=forms.TextInput(attrs={"placeholder": "اسمك"}),validators=[validate_feedback])
    email   = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder": "بريدك الالكترونى","type":"email"}))
    content = forms.CharField(label="",widget=forms.Textarea(attrs={"placeholder": "اترك رسالتك"}))

class addCommentForm(forms.Form):
    comment = forms.CharField(label="",required=True,widget=forms.Textarea(attrs={"placeholder": "رأيك يهمنا..."}))


class AddCommentForm(forms.Form):
    comment = forms.CharField(
        label="",
        required=True,
        widget=forms.Textarea(
            attrs={
                "placeholder": "رأيك يهمنا ...",
                "autocomplete": "off"
            }
        )
    )

class AddRateForm(forms.Form):
    rate_value  = forms.FloatField(label="", required=True,max_value=5,min_value=0)