import string
from datetime import date

from django.db import models
from django.utils import text, timezone

from .functions.date import to_date


class Todo(models.Model):
    """This class contains common fields for storing todos"""

    description = models.TextField()
    priority = models.CharField(max_length=1, choices={i: i for i in string.ascii_uppercase}, blank=True)
    recurrence = models.CharField(max_length=5, blank=True, null=True)

    start_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.summary

    @property
    def summary(self) -> str:
        """Returns a summary of the description (truncated to max. 20 words)"""
        return text.Truncator(self.description).words(20)

    @property
    def is_completed(self) -> bool:
        return self.completion_date is not None

    @property
    def length(self) -> int:
        """Returns the length (of days) between start and due date."""
        start = self.start_date or self.created.date()
        end = self.due_date

        if start and end and start < end:
            difference = end - start
            return difference.days

        return 0

    def save(self, *args, **kwargs):
        super(Todo, self).save(*args, **kwargs)

    def complete(self, completion_date: date = timezone.localdate()) -> None:
        self.completion_date = completion_date
        self.save()

    def postpone(self, pattern: str) -> None:
        """
        Postpones the todo based on the given pattern. Following rules are followed:

        * if due_date is set: new due_date = due_date + pattern
        * if start_date is set: new start_date = start_date + pattern
        * if no start_date is set: new start_date = today + pattern
        """

        if self.due_date:
            self.due_date = to_date(pattern, self.due_date)

        self.start_date = to_date(pattern, self.start_date)
        self.save()
