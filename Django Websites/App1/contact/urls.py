# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact, name='contact'),
    path('', views.home, name='home'),  # Map the root URL to the home view

]