from django import forms

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True,widget=forms.TextInput(attrs={"placeholder": "بريدك الإلكترونى"}))
    subject = forms.CharField(required=True,widget=forms.TextInput(attrs={"placeholder": "الموضوع"}))
    message = forms.CharField(required=True,widget=forms.Textarea(attrs={"placeholder": "اترك رسالتك*"}))
    
