from django.urls import path
from .views import ProjectListView, ProjectCreateView, ProjectDetailView, ProjectUpdateView, ProjectDeleteView, project_members

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('new/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_update'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('<int:pk>/members/', project_members, name='project_members'),
]
