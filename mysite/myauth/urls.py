from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (
    login_view,
    set_cookie_view,
    get_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutView,
    logout_view,
    AboutMeView,
    CreateUserView,
    HelloView,
)

app_name = "myauth"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("hello/", HelloView.as_view(), name="hello"),
    path("logout/", logout_view, name="logout"),
    path("about/", AboutMeView.as_view(), name="about_me"),
    path("register/", CreateUserView.as_view(), name="registry"),
    path("cookie/set", set_cookie_view, name="cookie_set"),
    path("cookie/get", get_cookie_view, name="cookie-get"),
    path("session/set", set_session_view, name="session_set"),
    path("session/get", get_session_view, name="session_get"),
]
