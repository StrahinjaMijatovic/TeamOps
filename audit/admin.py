from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'content_type', 'object_id', 'timestamp')
    list_filter = ('action', 'content_type')
    readonly_fields = ('user', 'action', 'content_type', 'object_id', 'timestamp', 'extra_data')
