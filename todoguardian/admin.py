from django.contrib import admin

from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    def completed(self, instance):
        return instance.is_completed

    completed.boolean = True
    completed.short_description = "Completed ?"

    date_hierarchy = "due_date"
    list_display = ["id", "description", "priority", "due_date", "start_date", "completed"]
    list_display_links = ["description"]
    list_filter = ["priority"]
    ordering = ["-due_date", "start_date", "priority"]
