from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    title = models.CharField(verbose_name="Category", max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return reverse("category_list", kwargs={"pk": self.pk})

class Article(models.Model):
    title = models.CharField(verbose_name="Title", max_length=255)
    description = models.TextField(verbose_name="Description")
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)
    viewed = models.PositiveIntegerField(verbose_name="Views", default=0)
    published_date = models.DateTimeField(verbose_name="The date of publication", auto_now_add=True)
    updated_date = models.DateTimeField(verbose_name="The date of update", auto_now_add=True)
    category = models.ForeignKey(Category, default=True, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    def trip_description(self):
        return self.description if len(str(self.description)) < 100 else self.description[:100] + "..."

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
