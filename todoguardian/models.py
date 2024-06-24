import re
import string
from datetime import date

from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import text, timezone
from pytodotxt import Task

from .functions.date import to_date


class Project(models.Model):
    """A project can be any type of collection of todos"""

    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Context(models.Model):
    """A context can be any type of similar todos or related todos"""

    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Todo(models.Model):
    """This class contains common fields for storing todos"""

    description = models.TextField()
    priority = models.CharField(max_length=1, choices={i: i for i in string.ascii_uppercase}, blank=True, null=True)
    recurrence = models.CharField(max_length=5, blank=True, help_text="Recurrence can be defined as a string ([0-9][bdwmy]), add + in front to have strict recurrence.")

    start_date = models.DateField(default=timezone.localdate)
    due_date = models.DateField(blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)
    _completed = models.BooleanField("completed?", default=False)

    projects = models.ManyToManyField(Project, blank=True, related_name="todos")
    contexts = models.ManyToManyField(Context, blank=True, related_name="todos")

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

    @property
    def is_overdue(self) -> bool:
        """Returns True if a todo is past due"""
        if self.due_date is not None:
            return timezone.localdate() > self.due_date

        return False

    @property
    def is_due_soon(self) -> bool:
        """Returns true if a todo is due in the next 3 days"""
        if self.due_date is not None:
            return timezone.localdate() + relativedelta(days=3) > self.due_date and timezone.localdate() <= self.due_date

        return False

    @property
    def due_date_code(self) -> int:
        """
        Returns a code representing due date for this todo.

        * -1: overdue
        * 0: due today
        * 1: due soon
        * 2: due later
        * 3: no due date
        """
        if self.is_overdue:
            return -1

        if self.due_date == timezone.localdate():
            return 0

        if self.is_due_soon:
            return 1

        if self.due_date is not None:
            return 2

        return 3

    @property
    def is_completed(self) -> bool:
        return self.completion_date is not None

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

        * If due_date:
            new due_date = today + pattern if due_date is passed else due_date + pattern
        * New start_date = today + pattern if start_date is passed or None else start_date + pattern
        """

        if self.due_date:
            distance = self.length

            if self.due_date < timezone.localdate():
                self.due_date = to_date(pattern)
            else:
                self.due_date = to_date(pattern, self.due_date)

            self.start_date = self.due_date - relativedelta(days=distance)

        else:
            if self.start_date > timezone.localdate():
                self.start_date = to_date(pattern, self.start_date)
            else:
                self.start_date = to_date(pattern)

        self.save()

    def to_string(self) -> str:
        """Returns a todo.txt compliant string"""
        task = Task(self.description)

        task.priority = self.priority
        task.is_completed = self.is_completed
        task.creation_date = self.created.date()

        if self.due_date is not None:
            task.add_attribute("due", self.due_date.isoformat())

        if self.start_date is not None:
            task.add_attribute("t", self.start_date.isoformat())

        if self.recurrence is not None and self.recurrence != "":
            task.add_attribute("rec", self.recurrence)

        for project in self.projects.all():
            task.add_project(text.slugify(project.name))

        for context in self.contexts.all():
            task.add_context(text.slugify(context.name))

        return str(task)

    to_string.short_description = "Todo.txt string"

    def update_from_string(self, string: str) -> None:
        """Updates the todo based on the information from the todo.txt string passed in."""
        task = Task(string)

        all_projects = {project.name: project for project in Project.objects.all()}
        all_contexts = {context.name: context for context in Context.objects.all()}

        self.description = task.bare_description()
        self.priority = task.priority
        self.completion_date = task.completion_date

        for attribute_key, attribute_values in task.attributes.items():
            match attribute_key:
                case "due":
                    self.due_date = to_date(attribute_values[0])

                case "rec":
                    self.recurrence = attribute_values[0]

                case "t" | "start":
                    self.start_date = to_date(attribute_values[0])

                case _:
                    continue

        self.save()

        self.projects.clear()
        self.contexts.clear()

        for project in task.projects:
            project = re.sub(r"-+", " ", project)

            if project in all_projects.keys():
                self.projects.add(all_projects[project])

            else:
                self.projects.create(name=project)

        for context in task.contexts:
            context = re.sub(r"-+", " ", context)

            if context in all_contexts.keys():
                self.contexts.add(all_contexts[context])

            else:
                self.contexts.create(name=context)

    @classmethod
    def from_string(cls, string: str) -> "Todo":
        """Converts a todo.txt compliant string into a new object"""
        todo = Todo.objects.create(description="New todo from string")
        todo.update_from_string(string)

        return todo


class Annotation(models.Model):
    """An annotation can be used to keep track of changes/statuses and notes for a given todo"""

    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name="annotations")
    text = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Annotation for todo {i.todo.id}".format(i=self)

    class Meta:
        get_latest_by = ["created"]
        ordering = ["-created"]
