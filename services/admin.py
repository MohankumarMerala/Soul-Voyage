from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ["title","category","duration","price","is_featured","order"]
    list_editable = ["is_featured","order","price"]
    prepopulated_fields = {"slug": ("title",)}
    list_filter   = ["category","is_featured"]
