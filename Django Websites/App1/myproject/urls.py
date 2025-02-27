from django.contrib import admin
from django.urls import path, include
from products.views import home  # Import the home view







urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('products/', include('products.urls')),
    path('au/', include('AU.urls')),
    path('contact/', include('contact.urls')),

  
]
