import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from manufacturer_site.inventory.models import RawMaterial, MaterialPurchaseLog
from manufacturer_site.production.models import Production
from manufacturer_site.classifications.models import Product
from manufacturer_site.cashier.models import Sale
from django.db.models import Sum, F, FloatField, ExpressionWrapper


@login_required
def dashboard(request):
    date_query = request.GET.get('d', '7')
    today = datetime.datetime.now()
    if date_query == 'mtd':
        start_date = datetime.datetime.strptime(
            today.strftime('%Y-%m-01'), '%Y-%m-%d')
    elif date_query == 'ytd':
        start_date = datetime.datetime.strptime(
            today.strftime('%Y-01-01'), '%Y-%m-%d')
    else:
        try:
            start_date = today - datetime.timedelta(days=int(date_query))
        except:
            messages.error(request, 'Invalid date range')
            return redirect('dashboard')

    raw_materials = RawMaterial.objects.all()
    products = Product.objects.all()
    productions = Production.objects.filter(date__range=[start_date, today])
    material_purchase_logs = MaterialPurchaseLog.objects.filter(
        date__range=[start_date, today])
    sales = Sale.objects.filter(order__date__range=[start_date, today])
    context = {
        'summary': _get_summary(materials=raw_materials, productions=productions, products=products, sales=sales, material_purchases=material_purchase_logs),
        'date_query': date_query,
        'date_filters': [
            ('7', '7 days'),
            ('mtd', 'This Month'),
            ('ytd', 'This Year'),
        ]
    }
    return render(request, 'manufacturer_site/dashboard/dashboard.html', context)


def _get_summary(materials, productions, products, sales, material_purchases) -> dict[str, any]:
    # MATERIAL SUMMARY
    materials_summary = materials.aggregate(stock_value=Sum(ExpressionWrapper(
        F('quantity_in_stock') * F('cost_price'), output_field=FloatField()
    )))

    # PRODUCTION SUMMARY
    ttl_batch_value = 0.0
    ttl_batch_cost = 0.0
    ttl_additional_costs = 0.0
    for production in productions:
        ttl_batch_cost += production.batch.ttl_cost
        for item in production.batch.batch_items.all():
            ttl_batch_value += (item.quantity_produced * item.selling_price)
        for resource in production.additional_resources.all():
            ttl_additional_costs += resource.ttl_cost

    # PRODUCT SUMMARY
    sellable_stock = products.aggregate(
        stock_value=Sum(ExpressionWrapper(
            F('quantity_in_stock') * F('selling_price'), output_field=FloatField()
        )))

    # SALES SUMMARY
    sales_summary = sales.aggregate(revenue=Sum('total_cost'))

    # EXPENSES SUMMARY
    material_purchases_summary = material_purchases.aggregate(
        total_cost=Sum('ttl_cost')
    )
    return {
        'ttl_stock_value': materials_summary['stock_value'] or 0.0,
        'ttl_batch_value': ttl_batch_value,
        'ttl_batch_cost': ttl_batch_cost,
        'sellable_stock_value': sellable_stock['stock_value'] or 0.0,
        'sales_revenue': sales_summary['revenue'] or 0.0,
        'ttl_expenses': (material_purchases_summary['total_cost'] or 0.0) + ttl_additional_costs,
    }
