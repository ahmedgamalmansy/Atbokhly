from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contact
from user_profile.models import UserProfile,ChiefProfile

def emailView(request):
    qs = ChiefProfile.objects.filter(user__username=request.user)
    context = {
        'profile_info': qs,
        'group': "chief"
    }
    if not qs:
        qs = UserProfile.objects.filter(user__username=request.user)
        context['profile_info'] = qs
        context['group'] = "user"
    if request.method == 'GET':
        form = ContactForm()
        context['form'] = form
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            Contact.objects.create(from_email=from_email, subject=subject, message=message)

            return redirect('contact:success')
    return render(request, "contact/email.html", context)

def successView(request):
    return render(request,'contact/contact_success.html',{})

def about(request,**kwargs):
    return render(request,'about.html',{})

def policies(request,**kwargs):
    return render(request,'policies.html',{})

