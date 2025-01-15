from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import RawMaterial
from django.db.models import Q
from .forms import RawMaterialForm
from django.contrib import messages


@login_required
def inventory(request):
    return redirect('product_inventory')


@login_required
def product_inventory(request):
    context = {}
    return render(request, 'manufacturer_site/inventory/product_inventory.html', context)


@login_required
def raw_materials(request):
    query = request.GET.get('q') or ''
    raw_materials = RawMaterial.objects.filter(
        Q(name__icontains=query) |
        Q(alias__icontains=query) |
        Q(code__icontains=query)
    )
    low_stock_raw_materials = RawMaterial.objects.filter(
        quantity_in_stock__lt=50)
    context = {
        'raw_materials': raw_materials,
        'low_stock_raw_materials': low_stock_raw_materials,
    }
    return render(request, 'manufacturer_site/inventory/raw_materials.html', context)


@login_required
def add_raw_materials(request):
    if request.method == 'POST':
        material_form = RawMaterialForm(request.POST)
        if material_form.is_valid():
            material_form.save()
            messages.success(request, 'Material has been added.')
            return redirect('raw_materials')
        else:
            messages.error(request, 'Invalid data entry.')
    else:
        material_form = RawMaterialForm()
    context = {
        'material_form': material_form,
    }
    return render(request, 'manufacturer_site/inventory/forms/create_raw_material.html', context)
