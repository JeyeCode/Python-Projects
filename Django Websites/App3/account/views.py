from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse



def shop_view(request):
    return render(request, 'account/shop.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome, {username}! Your account has been created.')

            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'account/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in!')  # Add success message
            return redirect('home.html')  # Redirect to homepage after login


        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'account/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

# shop view
from django.http import JsonResponse

def get_cart_items(request):
    # Assuming you have a session-based cart or a model for the cart
    cart = request.session.get('cart', {})
    
    if cart:
        # If there are items in the cart, return them
        return JsonResponse({'items': cart, 'message': 'Here are your cart items!'})
    else:
        # If the cart is empty, return a message
        return JsonResponse({'items': None, 'message': 'Your cart is empty!'})



