from django.contrib import admin

# Register your models here.
from .models import Article, Category

class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "trim_description", "viewed", "published_date", "updated_date", "category", "author")
    list_display_links = ("id", "title")
    list_editable = ("category", "author")
    list_filter = ("published_date", "category", "author")

    def trip_description(obj):
        return obj.description if len(str(self.description)) < 100 else self.description[:100] + "..."


admin.site.register(Article)
admin.site.register(Category)
