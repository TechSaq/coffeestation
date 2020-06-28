from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
# from django.conf.settings import production
from django.core.mail import send_mail

# Create your views here.


class HomeView(TemplateView):
    template_name = "index.html"

class ContactView(TemplateView):
    template_name = "contact.html"


def email(request):    
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = 'ans2sqb@gmail.com'
    # email_from = production.EMAIL_HOST_USER
    recipient_list = ['ansarimehtab22@gmail.com', ]    
    send_mail(subject, message, email_from, recipient_list)
    return redirect('core:home')

