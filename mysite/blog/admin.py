from django.contrib import admin

from blog.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "body", "published_at"]
