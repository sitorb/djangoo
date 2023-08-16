from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Article


class PostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            "title",
            "description",
            "photo",
            "category"
        )
        widgets = {
            # Заголовок
            "title": forms.TextInput(attrs={
                "class": "form-control"
            }),
            # Описание
            "description": forms.Textarea(attrs={
                "class": "form-control"
            }),
            # Фото выбор файла
            "photo": forms.FileInput(attrs={
                "class": "form-control"
            }),
            # Категория
            "category": forms.Select(attrs={
                "class": "form-select"
            })
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=150,
                               widget=forms.TextInput(attrs={
                                   "class": "form-control"
                               }))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        "class": "form-control"
    }))


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=150,
                               widget=forms.TextInput(attrs={
                                   "class": "form-control mb-3",
                                   "placeholder": "Username"
                               }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control mb-3",
        "placeholder": "Password"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control mb-3",
        "placeholder": "Confirm password"
    }))

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
