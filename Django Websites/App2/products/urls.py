# products/urls.py
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.products, name='products'),
    path('', views.home, name='home'),  # Map the root URL to the home view

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)