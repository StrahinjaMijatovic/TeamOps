from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q

from .models import Project
from tasks.models import Task
from audit.models import AuditLog

User = get_user_model()

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 9

    def get_queryset(self):
        # Show projects where user is owner OR member
        return Project.objects.filter(Q(owner=self.request.user) | Q(members=self.request.user)).distinct()

class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    fields = ['name', 'key', 'description']
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')

    def test_func(self):
        return self.request.user.can_edit

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['name', 'description', 'status']
    template_name = 'projects/project_form.html'

    def test_func(self):
        return self.request.user == self.get_object().owner

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.pk})

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')

    def test_func(self):
        return self.request.user == self.get_object().owner

@login_required
def project_members(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user != project.owner:
        return HttpResponseForbidden("Only the project owner can manage members.")

    available_users = User.objects.exclude(
        Q(pk=project.owner.pk) | Q(pk__in=project.members.all())
    )

    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        target_user = get_object_or_404(User, pk=user_id)

        if action == 'add':
            project.members.add(target_user)
            messages.success(request, f"{target_user.username} added to project.")
        elif action == 'remove':
            project.members.remove(target_user)
            messages.success(request, f"{target_user.username} removed from project.")

        return redirect('project_members', pk=project.pk)

    return render(request, 'projects/project_members.html', {
        'project': project,
        'available_users': available_users,
    })

class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def test_func(self):
        project = self.get_object()
        return self.request.user == project.owner or self.request.user in project.members.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object

        # Search & Filters
        query = self.request.GET.get('q')
        assignee_id = self.request.GET.get('assignee')

        tasks = Task.objects.filter(project=project)

        if query:
            tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))

        if assignee_id:
            tasks = tasks.filter(assignee_id=assignee_id)

        # Organize filtered tasks by column for display
        columns_with_tasks = []
        for column in project.board.columns.all():
            columns_with_tasks.append({
                'column': column,
                'tasks': tasks.filter(column=column)
            })
        context['columns_with_tasks'] = columns_with_tasks

        # Audit Log
        project_ct = ContentType.objects.get_for_model(Project)
        task_ct = ContentType.objects.get_for_model(Task)

        logs = AuditLog.objects.filter(
            Q(content_type=project_ct, object_id=project.id) |
            Q(content_type=task_ct, object_id__in=tasks.values_list('id', flat=True))
        ).select_related('user', 'content_type').order_by('-timestamp')[:20]

        context['audit_logs'] = logs
        return context
