from django.urls import path

from . import views

urlpatterns = [
    path('', views.core, name='home'),
    path('contact/', views.contact, name='contact'),
]
