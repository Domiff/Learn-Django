from django.contrib import admin

from shopapp.models import Product, Order
from .admin_mixins import ExportAsCSV


class OrderInline(admin.TabularInline):
    model = Product.orders.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSV):
    
    actions = (
        "export_csv",
    )
    
    inlines = (
        OrderInline,
    )
    list_display = "pk", "name", "description_short", "price"
    list_display_links = "pk", "name"
    search_fields = "name", "description"
    ordering = ("pk", "name")
    fieldsets = (
        (None, {
            "fields": ("name", "description")
        }),
        ("Price options", {
            "fields": ("price",),
            "classes": ("wide", "collapse"),
            "description": "Options for work with price"
        })
    )
    
    def description_short(self, obj: Product):
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."


class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
   
    inlines = (
        ProductInline,
    )
    
    list_display = ("addres", "created_at", "user_verbose")
    
    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order):
        return obj.user.first_name or obj.user.username
        