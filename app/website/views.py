from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
     return render(request, 'home.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # or redirect to another page
        else:
            # Handle invalid login
            return render(request, 'login.html', {'error': 'Invalid login'})
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, "Boli ste odhlásení")
    return redirect('login')


