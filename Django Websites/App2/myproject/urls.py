from django.contrib import admin
from django.urls import path, include
from products.views import home  # Import the home view
from django.shortcuts import redirect
from django.views.generic.base import RedirectView
from account import views  # Import the view from your account app



def redirect_to_login(request):
    return redirect('account/login/')

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('products/', include('products.urls')),
    path('au/', include('AU.urls')),
    path('account/', include('account.urls')),  # Include account app URLs
    path('', RedirectView.as_view(url='account/login/')),  # Redirect root to login page
    path('shop/', views.shop_view, name='shop'),  # Directly map shop/ to the view









]

