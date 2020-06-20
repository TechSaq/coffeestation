from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages

# Create your views here.


class HomeView(TemplateView):
    template_name = "index.html"

class ContactView(TemplateView):
    template_name = "contact.html"

