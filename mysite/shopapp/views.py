import logging
from csv import DictWriter

from django.http import HttpRequest, HttpResponse
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
    DetailView,
    ArchiveIndexView,
    DateDetailView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.auth.decorators import login_required
from docutils.nodes import field_name
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from .common import save_csv
from .models import Product, Order, ProductImage, BlogPost
from .forms import ProductForm
from .serializers import ProductSerializer

logger = logging.getLogger(__name__)


@extend_schema(description="Product API Set")
class ProductViewSet(viewsets.ModelViewSet):
    """"
    Hello man
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    search_fields = "name", "description",

    filterset_fields = [
        "name",
        "description",
        "price",
    ]
    ordering_fields = "pk", "name",


    @action(methods=["get"], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type="text/csv")
        file_name = "export_file.csv"
        response["Content-Disposition"] = f"attachment; filename={file_name}"
        queryset = self.filter_queryset(self.get_queryset())
        fields_name = [
            "name",
            "description",
            "price",
        ]
        queryset = queryset.only(*fields_name)
        writer = DictWriter(response, fieldnames=fields_name)
        writer.writeheader()

        for product in queryset:
            writer.writerow(
                {
                    field: getattr(product, field)
                    for field in fields_name
                }
            )
        return response

    @action(methods=["post"], detail=False, parser_classes=[MultiPartParser,] )
    def upload_csv(self, request: Request):
        products = save_csv(file=request.FILES["file"].file, encoding=request.encoding)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Blog posts",
        description="Param",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description="Parnas")
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class ShopIndexView(View):
    def get(self, request):
        products = [
            ("Laptop", 1999),
            ("Desktop", 3999),
            ("Phone", 199),
        ]

        context = {
            "products": products,
            "item": 0,
        }
        logger.info("Rendering template")
        return render(request, "shopapp/index.html", context=context)


class ShopDetailView(DetailView):
    # def get(self, request: HttpRequest, pk: int):
    #     product = get_object_or_404(Product, pk=pk)
    #     context = {
    #         "product": product,
    #     }
    #     return render(request, "shopapp/detail.html", context=context)

    template_name = "shopapp/detail.html"
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


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


class ProductViewList(PermissionRequiredMixin, ListView):
    permission_required = "view_product"
    model = Product
    template_name = "shopapp/products-list.html"
    context_object_name = "products"


# def products_list(request: HttpRequest):
#     context = {
#         "products": Product.objects.all(),
#     }
#     return render(request, "shopapp/products-list.html", context=context)
#


@login_required
def orders_list(request: HttpRequest):
    context = {
        "orders": Order.objects.select_related("user")
        .prefetch_related("products")
        .all()
    }
    return render(request, "shopapp/orders-list.html", context=context)


#
# def create_product(request: HttpRequest):
#     if request.method == "POST":
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             # Product.objects.create(**form.cleaned_data)
#             form.save()
#             url = reverse("shopapp:products")
#             return redirect(url)
#     else:
#         form = ProductForm()
#     context = {"forms": form}
#     return render(request, "shopapp/create-product.html", context=context)


class ProductCreate(UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_superuser

    model = Product
    fields = "name", "description", "price", "preview"
    success_url = reverse_lazy("shopapp:products")


class ProductUpdateView(UpdateView):
    model = Product
    # fields = "name", "description", "price", "preview"
    success_url = reverse_lazy("shopapp:products")
    template_name = "shopapp/product_update_form.html"
    form_class = ProductForm

    def get_success_url(self):
        return reverse("shopapp:products-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products")


class BlogArchiveIndexView(ArchiveIndexView):
    model = BlogPost
    date_field = "published_date"
    template_name = "shopapp/blog_archive.html"
    context_object_name = "dates"
