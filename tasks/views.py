from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Task
from .forms import TaskForm
from projects.models import Project, Board, Column

class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        is_member = self.request.user == self.project.owner or self.request.user in self.project.members.all()
        return is_member and self.request.user.can_edit

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.project
        return kwargs

    def form_valid(self, form):
        form.instance.project = self.project
        form.instance.created_by = self.request.user
        # Default to first column (To Do) if not specified
        if not form.instance.column_id:
            first_column = self.project.board.columns.first()
            form.instance.column = first_column
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.project.pk})

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'

    def test_func(self):
        task = self.get_object()
        is_member = self.request.user == task.project.owner or self.request.user in task.project.members.all()
        return is_member and self.request.user.can_edit

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.object.project
        return kwargs

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.project.pk})

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'

    def test_func(self):
        task = self.get_object()
        is_member = self.request.user == task.project.owner or self.request.user in task.project.members.all()
        return is_member and self.request.user.can_edit

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.project.pk})

@login_required
@require_POST
def update_task_column(request, pk):
    task = get_object_or_404(Task, pk=pk)
    column_id = request.POST.get('column_id')
    
    # Permission check: User must be member of project and not a viewer
    if request.user != task.project.owner and request.user not in task.project.members.all():
         return HttpResponseForbidden("You're not a member of this project.")
    if not request.user.can_edit:
         return HttpResponseForbidden("Viewers cannot modify tasks.")

    if column_id:
        column = get_object_or_404(Column, pk=column_id)
        if column.board == task.project.board:
             task.column = column
             task.save()
    
    return redirect('project_detail', pk=task.project.pk)
