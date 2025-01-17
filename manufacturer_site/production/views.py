from django.shortcuts import render


def productions(request):
    context = {}
    return render(request, 'manufacturer_site/production/productions.html')
