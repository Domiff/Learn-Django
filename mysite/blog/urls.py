from django.urls import path

from .views import ArticleListView, ArticleDetailView, LatestArticelsFeed

app_name =  "blog"


urlpatterns = [
    path("articles/", ArticleListView.as_view(), name="articles"),
    path("articles/<int:pk>/", ArticleDetailView.as_view(), name="article"),
    path("articles/latest/feed/", LatestArticelsFeed(), name="feed"),
]
