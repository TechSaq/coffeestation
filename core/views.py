from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
# from django.conf.settings import production
from django.core.mail import send_mail

# Create your views here.


class HomeView(View):

    def get(self, *args, **kwargs):
        context = {
            'home': True
        }
        return render(self.request, "index.html", context)

class ContactView(View):

    def get(self, *args, **kwargs):
        context = {
            'contact': True
        }
        return render(self.request, "contact.html", context)

    def post(self, *args, **kwargs):
        messages.success(
            self.request, "Your query has been received! Thanks for reaching us!")
        return redirect("core:home")




def email(request):    
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = 'ans2sqb@gmail.com'
    # email_from = production.EMAIL_HOST_USER
    recipient_list = ['ansarimehtab22@gmail.com', ]    
    send_mail(subject, message, email_from, recipient_list)
    return redirect('core:home')

