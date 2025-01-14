from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(
            request=request, username=username, password=password)
        if user is not None and user.is_authenticated:
            auth.login(request, user)
            messages.success(request, f'Welcome {user.username}')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
    else:
        username = ''
    context = {
        'username': username,
    }
    return render(request, 'auth_app/login.html', context)
