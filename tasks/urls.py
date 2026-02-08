from django.urls import path
from .views import TaskCreateView, TaskUpdateView, TaskDeleteView, update_task_column

urlpatterns = [
    path('project/<int:project_id>/create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('<int:pk>/move/', update_task_column, name='task_move'),
]
