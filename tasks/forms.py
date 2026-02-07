from django import forms
from django.db.models import Q
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assignee', 'priority', 'due_date', 'labels']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        if self.project:
            # Filter assignees to project members + owner
            self.fields['assignee'].queryset = User.objects.filter(
                Q(pk__in=self.project.members.all()) | Q(pk=self.project.owner.pk)
            )
