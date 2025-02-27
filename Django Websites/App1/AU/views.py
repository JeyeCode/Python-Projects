# products/views.py
# views.py
from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    return render(request, 'home.html')  # Render the home page template

def AU(request):
    return render(request, 'AU\AU.html')  # Render the products page template


