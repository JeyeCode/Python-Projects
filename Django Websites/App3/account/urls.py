from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('shop/', views.shop_view, name='shop'),
    path('get-cart-items/', views.get_cart_items, name='get_cart_items'),



]


