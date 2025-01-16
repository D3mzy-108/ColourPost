from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Packaging, ProductType
from .forms import PackagingForm, ProductTypeForm
from django.contrib import messages
from manufacturer_site.inventory.models import RawMaterial


@login_required
def classifications(request):
    return redirect('product_types')


# =============================================================
# =============================================================
# PRODUCT CATEGORY VIEWS
# =============================================================
# =============================================================
@login_required
def product_types(request):
    product_types = ProductType.objects.all()
    context = {
        'product_types': product_types,
    }
    return render(request, 'manufacturer_site/classifications/product_types.html', context)


@login_required
def add_product_category(request):
    if request.method == 'POST':
        product_category_form = ProductTypeForm(request.POST)
        if product_category_form.is_valid():
            product_category_form.save()
            messages.success(request, 'New product category has been created.')
            return redirect('product_types')
        else:
            messages.error(request, 'Invalid data entry.')
    else:
        product_category_form = ProductTypeForm()
    context = {
        'product_category_form': product_category_form,
    }
    return render(request, 'manufacturer_site/classifications/forms/create_product_type.html', context)


@login_required
def modify_product_category(request, id: int):
    product_category = get_object_or_404(ProductType, id=id)
    removed_material_id = request.GET.get('removeMaterialID')
    if removed_material_id is not None:
        material = get_object_or_404(RawMaterial, id=removed_material_id)
        product_category.raw_materials.remove(material)
        product_category.save()
        messages.info(
            request, f'{material} has been removed from production materials belonging to this category. This change will not affect past production records.')
        return redirect('modify_product_category', id=id)
    else:
        if request.method == 'POST':
            materials = RawMaterial.objects.filter(
                id__in=request.POST.getlist('raw_materials'))
            for material in materials:
                product_category.raw_materials.add(material)
            product_category.save()
            messages.success(
                request, 'Production materials for this category have been updated. This change will not affect past production records.')
            return redirect('modify_product_category', id=id)

    context = {
        'product_category': product_category,
        'raw_materials': RawMaterial.objects.all().exclude(id__in=product_category.raw_materials.all())
    }
    return render(request, 'manufacturer_site/classifications/forms/modify_product_type.html', context)


@login_required
def delete_product_category(request):
    category_id = request.GET.get('id')
    try:
        material = ProductType.objects.get(id=category_id)
        material.delete()
        messages.warning(
            request, 'Product type has been deleted.')
    except:
        messages.error(
            request, 'Failed to identify category ID.')
    return redirect('product_types')


# =============================================================
# =============================================================
# PRODUCT PACKAGING VIEWS
# =============================================================
# =============================================================
@login_required
def product_packaging(request):
    packages = Packaging.objects.all().order_by('volume')
    context = {
        'packages': packages,
    }
    return render(request, 'manufacturer_site/classifications/product_packaging.html', context)


@login_required
def add_package(request):
    if request.method == 'POST':
        packaging_form = PackagingForm(request.POST)
        if packaging_form.is_valid():
            packaging_form.save()
            messages.success(request, 'New package has been created.')
            return redirect('product_packaging')
        else:
            messages.error(request, 'Invalid data entry.')
    else:
        packaging_form = PackagingForm()
    context = {
        'packaging_form': packaging_form,
    }
    return render(request, 'manufacturer_site/classifications/forms/add_package.html', context)


@login_required
def delete_package(request):
    package_id = request.GET.get('id')
    try:
        material = Packaging.objects.get(id=package_id)
        material.delete()
        messages.warning(
            request, 'Package type has been removed.')
    except:
        messages.error(
            request, 'Failed to identify package ID.')
    return redirect('product_packaging')
