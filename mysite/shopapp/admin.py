from csv import DictReader

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path

from .common import save_csv
from .forms import CSVForm
from .models import Product, Order, ProductImage
from .admin_mixins import ExportAsCSV


class OrderInline(admin.TabularInline):
    model = Product.orders.through


class ProductImageInline(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSV):
    change_list_template = "shopapp/products-changelist.html"

    actions = ("export_csv",)

    inlines = (
        OrderInline,
        ProductImageInline,

    )
    list_display = "pk", "name", "description_short", "price"
    list_display_links = "pk", "name"
    search_fields = "name", "description"
    ordering = ("pk", "name")
    fieldsets = [
        (None, {"fields": ("name", "description")}),
        (
            "Price options",
            {
                "fields": ("price",),
                "classes": ("wide", "collapse"),
                "description": "Options for work with price",
            },
        ),
        (
            "Images",
            {
                "fields": ("preview",),
            },
        ),
    ]

    def description_short(self, obj: Product):
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVForm()
            context = {
                "form": form,
            }
            return render(request, "admin/import-csv.html", context)

        form = CSVForm(request.POST, request.FILES)

        # if form.is_valid():
        #     context = {
        #         "form": form,
        #     }
        #     return render(request, "admin/import-csv.html", context, status=400)

        save_csv(
            file = form.files["csv_file"].file,
            encoding=request.encoding,
        )

        reader = DictReader(csv_file)

        products = [
            Product(**row) for row in reader
        ]
        Product.objects.bulk_create(
            products,
            ignore_conflicts=True
        )
        self.message_user(request, "Good import")
        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("import-csv/", self.import_csv, name="import_csv")
        ]
        return new_urls + urls


class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (ProductInline,)

    list_display = ("addres", "created_at", "user_verbose")

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order):
        return obj.user.first_name or obj.user.username
