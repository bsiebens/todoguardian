import string
from datetime import date

from django.db import models
from django.utils import text, timezone

from .functions.date import to_date


class Todo(models.Model):
    """This class contains common fields for storing todos"""

    description = models.TextField()
    priority = models.CharField(max_length=1, choices={i: i for i in string.ascii_uppercase}, blank=True)
    recurrence = models.CharField(max_length=5, blank=True, null=True, help_text="Recurrence can be defined as a string ([0-9][bdwmy]), add + in front to have strict recurrence.")

    start_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)
    _completed = models.BooleanField("completed?", default=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.summary

    @property
    def summary(self) -> str:
        """Returns a summary of the description (truncated to max. 20 words)"""
        return text.Truncator(self.description).words(20)

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
        self._completed = self.completion_date is not None

        super(Todo, self).save(*args, **kwargs)

    def mark_complete(self, completion_date: date = timezone.localdate()) -> None:
        """Marks a todo as completed, using the supplied completion_date (default: today)"""
        self.completion_date = completion_date
        self.save()

    def mark_not_complete(self) -> None:
        """Marks a todo as not completed, removing any completion information."""
        self.completion_date = None
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

    def to_string(self) -> str:
        """Returns a todo.txt compliant string"""
        ...

    to_string.short_description = "Todo.txt string"

    @classmethod
    def from_string(cls, string: str) -> "Todo":
        """Converts a todo.txt compliant string into a new object"""
        ...
