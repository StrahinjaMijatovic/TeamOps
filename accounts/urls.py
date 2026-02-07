from django.urls import path, include
from .views import HomeView, RegisterView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
]
