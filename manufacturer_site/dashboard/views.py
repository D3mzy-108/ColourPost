from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    context = {}
    return render(request, 'manufacturer_site/dashboard/dashboard.html', context)
