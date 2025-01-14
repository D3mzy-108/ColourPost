from django.shortcuts import render, redirect


def classifications(request):
    return redirect('product_types')


def product_types(request):
    context = {}
    return render(request, 'manufacturer_site/classifications/product_types.html', context)


def product_packaging(request):
    context = {}
    return render(request, 'manufacturer_site/classifications/product_packaging.html', context)
