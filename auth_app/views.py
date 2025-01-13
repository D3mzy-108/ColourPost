from django.shortcuts import render


def login(request):
    context = {}
    return render(request, 'auth_app/login.html', context)
