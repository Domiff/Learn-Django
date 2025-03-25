from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.models import Group

from .models import Product, Order
from .forms import ProductForm

def shop_index(request: HttpRequest):
    products = [
        ("Laptop", 1999),
        ("Desktop", 3999),
        ("Phone", 199),
    ]
    
    context = {
        "products": products,
    }
    return render(request, 'shopapp/index.html', context=context)


def groups_list(request: HttpRequest):
    context ={
        "groups": Group.objects.prefetch_related('permissions').all()
    }
    return render(request, 'shopapp/groups_list.html', context=context)


def products_list(request: HttpRequest):
    context = {
        "products": Product.objects.all(),
    }
    return render(request, 'shopapp/products-list.html', context=context)


def orders_list(request: HttpRequest):
    context = {
        "orders": Order.objects.select_related("user").prefetch_related("products").all()
    }
    return render(request, 'shopapp/orders-list.html', context=context)


def create_product(request: HttpRequest):
    form = ProductForm
    context = { 
        "forms": form
    }
    return render(request, 'shopapp/create-product.html', context=context)