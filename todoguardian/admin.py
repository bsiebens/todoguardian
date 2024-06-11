from django.contrib import admin, messages
from django.utils import timezone
from django.utils.translation import ngettext

from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    @admin.action(description="Mark selected todos as completed")
    def mark_completed(self, request, queryset):
        updated = queryset.update(completion_date=timezone.localdate(), _completed=True)

        self.message_user(
            request,
            ngettext(
                "%d todo was marked as completed.",
                "%d todos were marked as completed.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    @admin.action(description="Mark selected todos as not completed")
    def mark_not_completed(self, request, queryset):
        updated = queryset.update(completion_date=None, _completed=False)

        self.message_user(
            request,
            ngettext(
                "%d todo was marked as not completed.",
                "%d todos were marked as not completed.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    date_hierarchy = "due_date"
    list_display = ["id", "description", "priority", "due_date", "start_date", "_completed"]
    list_display_links = ["description"]
    list_filter = ["_completed"]
    ordering = ["-due_date", "start_date", "priority"]
    actions = [mark_completed, mark_not_completed]
    search_fields = ["description"]
    readonly_fields = ["created", "modified", "to_string"]
    fieldsets = [
        [None, {"fields": ["description", ("priority", "recurrence")]}],
        ["DATES", {"fields": [("due_date", "start_date"), "completion_date"]}],
        ["GENERAL INFORMATION", {"fields": [("created", "modified"), "to_string"]}],
    ]
