from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ShopIndexView,
    groups_list,
    ProductViewList,
    ShopDetailView,
    orders_list,
    # create_product,
    ProductCreate,
    ProductUpdateView,
    ProductDeleteView,
    BlogArchiveIndexView, ProductViewSet,
)

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("groups/", groups_list, name="groups"),
    path("products/", ProductViewList.as_view(), name="products"),
    path("products/<int:pk>", ShopDetailView.as_view(), name="products-detail"),
    path(
        "products/<int:pk>/update", ProductUpdateView.as_view(), name="products-update"
    ),
    path(
        "products/<int:pk>/delete", ProductDeleteView.as_view(), name="products-delete"
    ),
    path("products/create", ProductCreate.as_view(), name="create_product"),
    path("orders", orders_list, name="orders"),
    path("products/form_create", ProductCreate.as_view(), name="create_product_form"),
    path("archive/", BlogArchiveIndexView.as_view(), name="blog_archive_index"),
    path("api/", include(routers.urls)),
]
