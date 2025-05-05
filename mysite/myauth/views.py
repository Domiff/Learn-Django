from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView
from django.utils.translation import gettext as _, ngettext

from .models import Profile


class HelloView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        welcome_message = _("Hello, world!")
        items_str = int(request.GET.get("items") or 0)
        items_line = ngettext(
            "one items",
            "{count} items",
            items_str
        )
        items_line = items_line.format(count=items_str)
        return HttpResponse(
            f"<h1>{welcome_message}</h1>"
            f"<p>{items_line}</p>"
        )


class AboutMeView(TemplateView):
    template_name = "myauth/about_me.html"


class CreateUserView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/create_user.html"
    success_url = reverse_lazy("myauth:about_me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user=user)
        return response


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            url = reverse("shopapp:products")
            return redirect(url)
        return render(request, "myauth/login.html")

    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect("shop/products")
    else:
        return render(request, "myauth/login.html")


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    _url = reverse("myauth:login")
    return redirect(_url)


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Set cookie")
    response.set_cookie("foo", "bar", max_age=3600)
    return response


# @permission_required("view_product", raise_exception=True)
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("foo", "default")
    return HttpResponse(f"Cookie value: {value!r}")


def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foo"] = "bar"
    return HttpResponse("Set session")


def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foo", "default")
    return HttpResponse(f"Session value: {value!r}")
