from typing import Any

from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext

from .functions.recurrence import NoRecurrenceException, advance_todo
from .models import Context, Project, Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    @admin.action(description="Mark selected todos as completed")
    def mark_completed(self, request, queryset):
        updated = queryset.update(completion_date=timezone.localdate(), _completed=True)

        for todo in queryset:
            try:
                advance_todo(todo)
            except NoRecurrenceException:
                pass

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

    def list_projects(self, instance) -> str:
        projects = [project.name for project in instance.projects.order_by("name")]

        return mark_safe("<br />".join(projects))

    list_projects.short_description = "Projects"

    def list_contexts(self, instance) -> str:
        contexts = [context.name for context in instance.contexts.order_by("name")]

        return mark_safe("<br />".join(contexts))

    list_contexts.short_description = "Contexts"

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)

        return queryset.prefetch_related("projects", "contexts")

    date_hierarchy = "due_date"
    list_display = ["id", "description", "priority", "due_date", "start_date", "_completed", "list_projects", "list_contexts"]
    list_display_links = ["description"]
    list_filter = ["_completed", "projects", "contexts"]
    ordering = ["due_date", "start_date", "priority"]
    actions = [mark_completed, mark_not_completed]
    search_fields = ["description"]
    readonly_fields = ["created", "modified", "to_string"]
    filter_horizontal = ["projects", "contexts"]
    fieldsets = [
        [None, {"fields": ["description", ("priority", "recurrence"), "projects", "contexts"]}],
        ["DATES", {"fields": [("due_date", "start_date"), "completion_date"]}],
        ["GENERAL INFORMATION", {"fields": [("created", "modified"), "to_string"]}],
    ]


admin.site.register(Project)
admin.site.register(Context)
