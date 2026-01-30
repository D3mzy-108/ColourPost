from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import RawMaterial, MaterialPurchaseLog
from manufacturer_site.classifications.models import Product
from django.db.models import Q, ExpressionWrapper, F, FloatField, Sum
from .forms import RawMaterialForm, MaterialPurchaseLogForm, ProductForm
from django.contrib import messages


@login_required
def inventory(request):
    return redirect('product_inventory')


@login_required
def product_inventory(request):
    products = Product.objects.all().annotate(
        market_value=ExpressionWrapper(
            F('selling_price') * F('quantity_in_stock'), output_field=FloatField()),
        true_value=ExpressionWrapper(F('cost_price') * F('quantity_in_stock'), output_field=FloatField())).order_by('-id')
    inventory_summary = products.aggregate(
        total_market_value=Sum(ExpressionWrapper(
            F('selling_price') * F('quantity_in_stock'), output_field=FloatField())),
        total_true_value=Sum(ExpressionWrapper(
            F('cost_price') * F('quantity_in_stock'), output_field=FloatField())))

    context = {
        'products': products,
        'inventory_summary': inventory_summary,
    }
    print(context)
    return render(request, 'manufacturer_site/inventory/product_inventory.html', context)


@login_required
def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        selling_price = request.POST.get('selling_price')
        product.selling_price = selling_price
        product.image = request.FILES.get('image')
        product.save()
        messages.success(request, f'Changes to {product} has been saves.')
        return redirect('product_details', id)
    context = {
        'product': product,
    }
    return render(request, 'manufacturer_site/inventory/product_inventory/product_details.html', context)


@login_required
def new_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, 'New product has been added.')
            return redirect('product_inventory')
    else:
        product_form = ProductForm()
    context = {
        'product_form': product_form,
    }
    return render(request, 'manufacturer_site/inventory/forms/new_product.html', context)


@login_required
def raw_materials(request):
    query = request.GET.get('q') or ''
    raw_materials = RawMaterial.objects.filter(
        Q(name__icontains=query) |
        Q(alias__icontains=query) |
        Q(code__icontains=query)
    ).annotate(total_value=ExpressionWrapper(F('quantity_in_stock') * F('cost_price'), output_field=FloatField())).order_by('-id')
    low_stock_raw_materials = RawMaterial.objects.filter(
        quantity_in_stock__lt=50).order_by('-id')
    context = {
        'raw_materials': raw_materials,
        'low_stock_raw_materials': low_stock_raw_materials,
        'inventory_summary': raw_materials.aggregate(stock_value=Sum('total_value')),
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


@login_required
def delete_raw_material(request):
    material_id = request.GET.get('id')
    try:
        material = RawMaterial.objects.get(id=material_id)
        material.delete()
        messages.warning(
            request, 'Raw material and all related records have been deleted.')
    except:
        messages.error(
            request, 'Failed to identify material ID.')
    return redirect('raw_materials')


@login_required
def material_purchase_log(request):
    material_purchases = MaterialPurchaseLog.objects.all().order_by('-date')
    context = {
        'material_purchases': material_purchases,
    }
    return render(request, 'manufacturer_site/inventory/raw_materials/purchase_log.html', context)


@login_required
def create_purchase_log(request):
    material_id = request.GET.get('mid')
    if material_id is not None:
        selected_material = get_object_or_404(RawMaterial, id=material_id)
    else:
        selected_material = None

    if request.method == 'POST':
        if selected_material is not None:
            instance = request.POST.copy()
            instance.update({'raw_material': selected_material.id})
            purchase_log_form = MaterialPurchaseLogForm(instance)
        else:
            purchase_log_form = MaterialPurchaseLogForm(request.POST)
        if purchase_log_form.is_valid():
            purchase_log_form.save()
            messages.success(
                request, 'Purchase has been logged, and the material involved has been updated.')
            return redirect('raw_materials')
        else:
            messages.error(request, 'Invalid data entry')
    else:
        purchase_log_form = MaterialPurchaseLogForm()
    context = {
        'purchase_log_form': purchase_log_form,
        'selected_material': selected_material,
    }
    return render(request, 'manufacturer_site/inventory/forms/create_purchase_log.html', context)
