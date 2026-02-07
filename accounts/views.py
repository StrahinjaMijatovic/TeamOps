from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import User

class HomeView(TemplateView):
    template_name = "home.html"

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"

class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_admin

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role_choices'] = User.Role.choices
        return context

@login_required
def user_role_update(request, pk):
    if not request.user.is_admin:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Only admins can change roles.")

    target_user = get_object_or_404(User, pk=pk)

    if target_user == request.user:
        messages.error(request, "You cannot change your own role.")
        return redirect('user_list')

    if request.method == 'POST':
        new_role = request.POST.get('role')
        if new_role in dict(User.Role.choices):
            target_user.role = new_role
            target_user.save(update_fields=['role'])
            messages.success(request, f"Role for {target_user.username} changed to {target_user.get_role_display()}.")
        else:
            messages.error(request, "Invalid role.")

    return redirect('user_list')
