import random
import string
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Production, ProductionResource, ProductionBatch, BatchItem
from manufacturer_site.classifications.models import ProductType, Product
from manufacturer_site.inventory.models import RawMaterial
from django.db.models import Q


def _generate_random_string(length: int) -> str:
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(length))


def _active_steps(production_id) -> int:
    value = 1
    if not ProductionResource.objects.filter(production__id=production_id, quantity_used__lte=0).exists():
        value = 2
    if not ProductionBatch.objects.filter(production__id=production_id, volume_produced=0).exists():
        value = 3
    return value


# =====================================================================
# =====================================================================
# PRODUCTIONs LIST
# =====================================================================
# =====================================================================


@login_required
def productions(request):
    productions = Production.objects.all()
    context = {
        'productions': productions,
    }
    return render(request, 'manufacturer_site/production/productions.html', context)


@login_required
def new_production(request):
    if request.method == 'POST':
        product_type = request.POST.get('product_type')

        # CREATE PRODUCTION INSTANCE
        production = Production()
        production.product_type = get_object_or_404(
            ProductType, id=product_type)
        today = datetime.today()
        year = str(today.year)[-2:]
        month = str(today.month).zfill(2)
        day = str(today.day).zfill(2)
        production.production_code = f'CP{_generate_random_string(3)}{year}{month}{day}'
        production.save()

        # CREATE BATCH INSTANCE
        batch = ProductionBatch()
        batch.production = production
        batch.save()

        # CREATE INSTANCES OF PRODUCTION RESOURCES
        for material in production.product_type.raw_materials.all():
            resource = ProductionResource()
            resource.production = production
            resource.material = material
            resource.save()

        messages.success(request, 'New production started.')
        return redirect('production_details', production.id)

    product_types = ProductType.objects.all()
    context = {
        'product_types': product_types,
    }
    return render(request, 'manufacturer_site/production/forms/new_production.html', context)


@login_required
def delete_production(request):
    production_id = request.GET.get('id')
    production = get_object_or_404(Production, id=production_id)
    if not production.is_completed:
        production.delete()
        messages.info(
            request, f'{production.production_code} production environment has been deleted')
    else:
        messages.error(
            request, f'Production environment has already been closed')
    return redirect('productions')


@login_required
def navigate_production_environment(request, production_id, tab):
    if tab == 1:
        return redirect('production_details', production_id)
    elif tab == 2:
        return redirect('batch_details', production_id)
    elif tab == 3:
        return redirect('packaging_details', production_id)


# =====================================================================
# =====================================================================
# PRODUCTION DETAILS
# =====================================================================
# =====================================================================

@login_required
def production_details(request, production_id):
    production = get_object_or_404(Production, id=production_id)
    resources = ProductionResource.objects.filter(production__id=production_id)
    if request.method == 'POST':
        for resource in resources:
            qty = request.POST.get(f'quantity_used_{resource.id}')
            resource.quantity_used = float(f"{qty}")
            resource.save()
        else:
            messages.success(
                request, "Changes to production resources has been saved.")
            return redirect('production_details', production_id)

    context = {
        'production': production,
        'next_tab': 2,
        'active_step': _active_steps(production_id),
    }
    return render(request, 'manufacturer_site/production/production_details.html', context)


@login_required
def add_production_resource(request, production_id):
    production = get_object_or_404(Production, id=production_id)
    resources = ProductionResource.objects.filter(production__id=production_id)
    query = request.GET.get('q') or ''
    mid = request.GET.get('mid')
    if mid is not None:
        material = get_object_or_404(RawMaterial, id=mid)
        production_resource = ProductionResource()
        production_resource.production = production
        production_resource.material = material
        production_resource.save()
        messages.success(
            request, f'{material.name} has been added to production resources.')
        return redirect(request.META.get('HTTP_REFERER'))
    included_materials_list = [
        resource.material.id for resource in resources
    ]
    excluded_materials = RawMaterial.objects.filter(
        Q(name__icontains=query) |
        Q(alias__icontains=query) |
        Q(code__icontains=query)
    ).exclude(id__in=included_materials_list)

    context = {
        'production': production,
        'excluded_materials': excluded_materials,
    }
    return render(request, 'manufacturer_site/production/forms/add_resources.html', context)


@login_required
def remove_production_resource(request):
    resource_id = request.GET.get('id')
    resource = get_object_or_404(ProductionResource, id=resource_id)
    if not resource.production.is_completed:
        resource.delete()
        messages.info(
            request, f'{resource.material} has been removed from production resources')
    else:
        messages.error(
            request, f'Production environment has already been closed')
    return redirect('production_details', resource.production.id)


# =====================================================================
# =====================================================================
# PRODUCTION BATCHING
# =====================================================================
# =====================================================================


@login_required
def batch_details(request, production_id):
    production = get_object_or_404(Production, id=production_id)
    if _active_steps(production_id) < 2:
        messages.warning(
            request, 'You have not set the quantity used for some of the production resources.')
        return redirect('production_details', production_id)

    batch = ProductionBatch.objects.get(production=production)
    if request.method == 'POST':
        volume_produced = request.POST.get('volume_produced')
        batch.volume_produced = volume_produced
        batch.save()
        messages.success(request, 'Batch information updated')
        return redirect('batch_details', production_id)

    context = {
        'production': production,
        'batch': batch,
        'next_tab': 3,
        'prev_tab': 1,
        'active_step': _active_steps(production_id),
    }
    return render(request, 'manufacturer_site/production/batch_details.html', context)


# =====================================================================
# =====================================================================
# PRODUCTION PACKAGING
# =====================================================================
# =====================================================================


@login_required
def packaging_details(request, production_id):
    production = get_object_or_404(Production, id=production_id)
    if _active_steps(production_id) < 3:
        messages.warning(
            request, 'Set the volume produced in this batch')
        return redirect('packaging_details', production_id)

    total_recorded_volume = 0
    for item in production.batch.batch_items.all():
        total_recorded_volume += item.total_volume

    if request.method == 'POST':
        for item in production.batch.batch_items.all():
            qty = request.POST.get(f'quantity_produced_{item.id}')
            item.quantity_produced = float(f"{qty}")
            item.save()
        else:
            messages.success(
                request, "Changes to production batch items have been saved.")
            return redirect('packaging_details', production_id)

    context = {
        'production': production,
        'prev_tab': 2,
        'active_step': _active_steps(production_id),
        'total_recorded_volume': total_recorded_volume,
    }
    return render(request, 'manufacturer_site/production/packaging_details.html', context)


@login_required
def add_package_item(request, production_id):
    production = get_object_or_404(Production, id=production_id)
    included_products = production.batch.batch_items.all()
    query = request.GET.get('q') or ''
    pid = request.GET.get('pid')
    if pid is not None:
        product = get_object_or_404(Product, id=pid)
        batch_item = BatchItem()
        batch_item.batch = production.batch
        batch_item.product = product
        batch_item.save()
        messages.success(
            request, f'{product} has been added to production batch items.')
        return redirect(request.META.get('HTTP_REFERER'))
    included_materials_list = [
        item.product.id for item in included_products
    ]
    excluded_materials = Product.objects.filter(
        Q(product_type__name__icontains=query)
    ).exclude(id__in=included_materials_list)

    context = {
        'production': production,
        'excluded_materials': excluded_materials,
    }
    return render(request, 'manufacturer_site/production/forms/add_package_item.html', context)


@login_required
def remove_package_item(request):
    item_id = request.GET.get('id')
    item = get_object_or_404(BatchItem, id=item_id)
    if not item.batch.production.is_completed:
        item.delete()
        messages.info(
            request, f'{item.product} has been removed from production batch items')
    else:
        messages.error(
            request, f'Production environment has already been closed')
    return redirect('packaging_details', item.batch.production.id)
