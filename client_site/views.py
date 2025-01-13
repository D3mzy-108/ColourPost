from django.shortcuts import render


def home(request):
    context = {}
    return render(request, 'client_site/home.html', context)
