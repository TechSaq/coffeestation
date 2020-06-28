from django.urls import path

from .views import HomeView, ContactView, email


app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('email/', email, name='email'),

]
