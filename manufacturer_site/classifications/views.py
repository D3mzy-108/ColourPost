from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Packaging
from .forms import PackagingForm
from django.contrib import messages


@login_required
def classifications(request):
    return redirect('product_types')


@login_required
def product_types(request):
    context = {}
    return render(request, 'manufacturer_site/classifications/product_types.html', context)


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
