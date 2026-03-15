from django.contrib import admin
from .models import ConsultationRequest

@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display    = ('name', 'email', 'phone', 'submitted_at', 'is_read')
    list_filter     = ('is_read', 'submitted_at')
    search_fields   = ('name', 'email', 'phone')
    readonly_fields = ('name', 'email', 'phone', 'message', 'submitted_at')
    list_editable   = ('is_read',)

    def has_add_permission(self, request):
        return False