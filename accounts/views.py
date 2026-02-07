from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm

class HomeView(TemplateView):
    template_name = "home.html"

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"
