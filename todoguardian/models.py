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
    priority = models.CharField(max_length=1, choices={i: i for i in string.ascii_uppercase}, blank=True)
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
        return timezone.localdate() > self.due_date

    @property
    def is_due_soon(self) -> bool:
        """Returns true if a todo is due in the next 3 days"""
        return timezone.localdate() + relativedelta(days=3) > self.due_date and timezone.localdate() <= self.due_date

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

        return str(task)

    to_string.short_description = "Todo.txt string"

    @classmethod
    def from_string(cls, string: str) -> "Todo":
        """Converts a todo.txt compliant string into a new object"""
        task = Task(string)
        todo = Todo.objects.create(description=task.bare_description(), priority=task.priority, completion_date=task.completion_date)

        all_projects = {project.name: project for project in Project.objects.all()}
        all_contexts = {context.name: context for context in Context.objects.all()}

        for attribute_key, attribute_values in task.attributes.items():
            match attribute_key:
                case "due":
                    todo.due_date = to_date(attribute_values[0])

                case "rec":
                    todo.recurrence = attribute_values[0]

                case "t" | "start":
                    todo.start_date = to_date(attribute_values[0])

                case _:
                    continue

        for project in task.projects:
            if project in all_projects.keys():
                todo.projects.add(all_projects[project])

            else:
                todo.projects.create(name=project)

        for context in task.contexts:
            if context in all_contexts.keys():
                todo.contexts.add(all_contexts[context])

            else:
                todo.contexts.create(name=context)

        return todo

        """  projects = {project.name: project for project in Project.objects.all()}
        contexts = {context.name: context for context in Context.objects.all()}

        for project in task.projects:
            projects_to_add = []

            # First check to see if object is already cached
            if project in projects.keys():
                projects_to_add.append(projects[project])
            else:
                projects_to_add.append(Project.objects.create(name=project))

            todo.projects.set(projects_to_add)

        for context in task.contexts:
            contexts_to_add = []

            # First check to see if object is already cached
            if context in contexts.keys():
                contexts_to_add.append(contexts[context])
            else:
                contexts_to_add.append(Context.objects.create(name=context))

            todo.contexts.set(contexts_to_add)

        for attribute, values in task.attributes.items():
            match attribute:
                case "due":
                    # First see if it matches a pattern
                    date = to_date(values[0])
                    if date is not None:
                        todo.due_date = date

                    else:
                        todo.due_date = values[0]

                case "rec":
                    todo.recurrence = values[0]

                case "t" | "start":
                    # First see if it matches a pattern
                    date = to_date(values[0])
                    if date is not None:
                        todo.start_date = date

                    else:
                        todo.start_date = values[0]

                case _:
                    continue

        return todo"""
