from django.urls import path
from .views import ProjectListView, ProjectCreateView, ProjectDetailView, ProjectUpdateView

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('new/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_update'),
]
