# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('AU/', views.AU, name='AU'),

]