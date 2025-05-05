from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.contrib.syndication.views import Feed

from .models import Article


class ArticleListView(ListView):
    queryset = (Article.objects.
                filter(published_at__isnull=False).
                order_by("-published_at"))
    template_name = "blog/list-article.html"


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/article-detail.html"
    context_object_name = "article"


class LatestArticelsFeed(Feed):
    title = "Python for beginners"
    description = "The best article"
    link = reverse_lazy("blog:articles")

    def items(self):
        return (Article.objects.
                filter(published_at__isnull=False).
                order_by("-published_at"))

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.body[:200]
