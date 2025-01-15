from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def classifications(request):
    return redirect('product_types')


@login_required
def product_types(request):
    context = {}
    return render(request, 'manufacturer_site/classifications/product_types.html', context)


@login_required
def product_packaging(request):
    context = {}
    return render(request, 'manufacturer_site/classifications/product_packaging.html', context)
