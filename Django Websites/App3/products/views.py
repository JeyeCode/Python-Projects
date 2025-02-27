# products/views.py
# views.py
from django.shortcuts import render
from django.http import JsonResponse


def home(request):
    return render(request, 'home.html')  # Render the home page template

def products(request):
    return render(request, 'products/products.html')  # Render the products page template

