from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def inventory(request):
    return redirect('product_inventory')


@login_required
def product_inventory(request):
    context = {}
    return render(request, 'manufacturer_site/inventory/product_inventory.html')


@login_required
def raw_materials(request):
    context = {}
    return render(request, 'manufacturer_site/inventory/raw_materials.html')
