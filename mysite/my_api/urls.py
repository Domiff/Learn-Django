from django.urls import path

from .views import view_api, GroupView

app_name = "my_api"


urlpatterns = [
    path("", view_api, name="api"),
    path("group/", GroupView.as_view(), name="group"),
]