from django.urls import path, include
from .views import HomeView, RegisterView, UserListView, user_role_update

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/users/', UserListView.as_view(), name='user_list'),
    path('accounts/users/<int:pk>/role/', user_role_update, name='user_role_update'),
    path('accounts/', include('django.contrib.auth.urls')),
]
