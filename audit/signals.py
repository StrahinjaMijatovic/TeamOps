import json
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import AuditLog
from projects.models import Project
from tasks.models import Task

TRACKED_FIELDS = {
    Project: ['name', 'description', 'status'],
    Task: ['title', 'description', 'column', 'assignee', 'priority', 'due_date'],
}

def create_audit_log(sender, instance, action, user=None, extra_data=None, **kwargs):
    if not user:
        if hasattr(instance, 'created_by') and instance.created_by:
            user = instance.created_by
        elif hasattr(instance, 'owner') and instance.owner:
            user = instance.owner

    AuditLog.objects.create(
        user=user,
        action=action,
        content_object=instance,
        extra_data=extra_data,
    )

@receiver(pre_save, sender=Project)
@receiver(pre_save, sender=Task)
def capture_old_values(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    changes = {}
    for field in TRACKED_FIELDS.get(sender, []):
        old_val = getattr(old, field)
        new_val = getattr(instance, field)
        if old_val != new_val:
            changes[field] = {
                'old': str(old_val) if old_val is not None else None,
                'new': str(new_val) if new_val is not None else None,
            }

    instance._audit_changes = changes

@receiver(post_save, sender=Project)
@receiver(post_save, sender=Task)
def log_save(sender, instance, created, **kwargs):
    if created:
        create_audit_log(sender, instance, AuditLog.Action.CREATED)
    else:
        changes = getattr(instance, '_audit_changes', {})
        extra_data = json.dumps(changes) if changes else None
        create_audit_log(sender, instance, AuditLog.Action.UPDATED, extra_data=extra_data)

@receiver(post_delete, sender=Project)
@receiver(post_delete, sender=Task)
def log_delete(sender, instance, **kwargs):
    create_audit_log(sender, instance, AuditLog.Action.DELETED)
