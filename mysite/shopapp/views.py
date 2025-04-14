from django.db.migrations import CreateModel
from django.http import HttpRequest
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Product, Order
from .forms import ProductForm


class ShopIndexView(View):
    def get(self, request):
        products = [
            ("Laptop", 1999),
            ("Desktop", 3999),
            ("Phone", 199),
        ]

        context = {
            "products": products,
        }
        return render(request, "shopapp/index.html", context=context)


class ShopDetailView(View):
    def get(self, request: HttpRequest, pk: int):
        product = get_object_or_404(Product, pk=pk)
        context = {
            "product": product,
        }
        return render(request, "shopapp/detail.html", context=context)


def groups_list(request: HttpRequest):
    context = {"groups": Group.objects.prefetch_related("permissions").all()}
    return render(request, "shopapp/groups_list.html", context=context)


# class ProductListView(TemplateView):
#     template_name = "shopapp/products-list.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["products"] = Product.objects.all()
#         return context


class ProductViewList(ListView):
    model = Product
    template_name = "shopapp/products-list.html"
    context_object_name = "products"


# def products_list(request: HttpRequest):
#     context = {
#         "products": Product.objects.all(),
#     }
#     return render(request, "shopapp/products-list.html", context=context)
#


def orders_list(request: HttpRequest):
    context = {
        "orders": Order.objects.select_related("user")
        .prefetch_related("products")
        .all()
    }
    return render(request, "shopapp/orders-list.html", context=context)


def create_product(request: HttpRequest):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            # Product.objects.create(**form.cleaned_data)
            form.save()
            url = reverse("shopapp:products")
            return redirect(url)
    else:
        form = ProductForm()
    context = {"forms": form}
    return render(request, "shopapp/create-product.html", context=context)


class ProductCreate(CreateView):
    model = Product
    fields = "name", "description", "price"
    success_url = reverse_lazy("shopapp:products")


class ProductUpdateView(UpdateView):
    model = Product
    fields = "name", "description", "price"
    success_url = reverse_lazy("shopapp:products")
    template_name = "shopapp/product_update_form.html"

    def get_success_url(self):
        return reverse("shopapp:products", kwargs={"pk": self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products")
