from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import AuditLog
from projects.models import Project
from tasks.models import Task

def create_audit_log(sender, instance, action, user=None, **kwargs):
    # Try to find user from instance if available (e.g. created_by field)
    if not user:
        if hasattr(instance, 'created_by') and instance.created_by:
            user = instance.created_by
        elif hasattr(instance, 'owner') and instance.owner:
            user = instance.owner
            
    AuditLog.objects.create(
        user=user,
        action=action,
        content_object=instance
    )

@receiver(post_save, sender=Project)
@receiver(post_save, sender=Task)
def log_save(sender, instance, created, **kwargs):
    action = AuditLog.Action.CREATED if created else AuditLog.Action.UPDATED
    create_audit_log(sender, instance, action)

@receiver(post_delete, sender=Project)
@receiver(post_delete, sender=Task)
def log_delete(sender, instance, **kwargs):
    create_audit_log(sender, instance, AuditLog.Action.DELETED)
