from django.urls import path

from .views import get_request_method, get_post, upload_file


app_name = "requestdataapp"

urlpatterns = [
   path("get/", get_request_method, name="get-request"),
   path("form/", get_post, name="form"),
   path("up/", upload_file, name="upload"),
]