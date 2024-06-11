from django.contrib import admin

from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    date_hierarchy = "due_date"
    list_display = ["id", "description", "priority", "due_date", "start_date", "_completed"]
    list_display_links = ["description"]
    list_filter = ["_completed"]
    ordering = ["-due_date", "start_date", "priority"]
