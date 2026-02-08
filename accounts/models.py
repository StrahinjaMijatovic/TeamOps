from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        TEAM_MEMBER = "TEAM_MEMBER", "Team Member"
        VIEWER = "VIEWER", "Viewer"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.TEAM_MEMBER)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_viewer(self):
        return self.role == self.Role.VIEWER

    @property
    def can_edit(self):
        return self.role in (self.Role.ADMIN, self.Role.TEAM_MEMBER)
