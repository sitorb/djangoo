from django.shortcuts import render, redirect
from .models import Article, Category
from .forms import LoginForm, RegistrationForm, PostForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
# PYTHON MANAGE.PY RUNSERVER


# def index_view(request):
#     articles = Article.objects.all()
#     context = {
#         "articles": articles
#     }
#     return render(request, "pages/index.html", context)

class Index(ListView):
    model = Article
    context_object_name = "articles"
    template_name = "pages/index.html"

# def categories_list(request, pk):
#     articles = Article.objects.filter(category_id=pk)
#     context = {
#         "articles": articles
#     }
#     return render(request, "blog/pages/index.html", context)

class ArticleByCategory(Index):
    def get_queryset(self):
        return Article.objects.filter(category_id=self.kwargs["pk"])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category =Category.objects.get(pk=self.kwargs["pk"])
        return context

# def article_detail(request, pk):
#     article = Article.objects.get(pk=pk)
#     title = article.title
#     context = {
#         "article": article,
#         "title": title
#     }
#     return render(request, "pages/article.html", context)

class ArticleDetail(DetailView):
    model = Article
    template_name = "blog/pages/article.html"

    def get_queryset(self):
        return Article.objects.filter(pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article = Article.objects.get(pk=self.kwargs["pk"])
        article.viewed += 1
        article.save()
        context['title'] = f"Article: {article.title}"
        return context

def sign_in(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "u successfully signed in, good for uuu")
            return redirect('home')
    else:
        form = LoginForm()
    context = {
        "form": form
    }
    return render(request, "blog/pages/sign-in.html", context)

def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            #login(request, user)
            return redirect('sign_in')
    else:
        form = RegistrationForm()
    context = {
        "form": form
    }
    return render(request, "blog/pages/sign-up.html", context)


def user_logout(request):
    logout(request)
    return redirect("home")


class SearchResults(Index):
    def get_queryset(self):
        word = self.request.GET.get('q')
        articles = Article.objects.filter(
            Q(title__icontains=word) | Q(description__icontains=word)
        )
        return articles


# def add_post(request):
#     if request.method == "POST":
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             article = Article.objects.create(**form.cleaned_data)
#             article.save()
#             return redirect("article_detail", article.pk)
#
#     else:
#         form = PostForm()
#
#     context = {
#         "form": form
#     }
#     return render(request, "pages/article_form.html", context)

class NewArticle(CreateView, LoginRequiredMixin):
    form_class = PostForm
    template_name = "blog/pages/article_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePost(UpdateView,  LoginRequiredMixin):
    model = Article
    form_class = PostForm
    template_name = "blog/pages/article_form.html"

class DeletePost(DeleteView, LoginRequiredMixin):
    model = Article
    success_url = reverse_lazy("home")
    context_object_name = "article"
    template_name = "blog/pages/article_confirm_delete.html"

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_superuser or self.request.user != Article.author:
            return redirect("home")