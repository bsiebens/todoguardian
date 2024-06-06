from django.db import models
import string
from dateutil.relativedelta import relativedelta
from django.utils import timezone, text
from .date_functions import convert_pattern_to_date
from datetime import date
from .exceptions import NoRecurrenceException


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
            self.due_date = convert_pattern_to_date(pattern, self.due_date)

        self.start_date = convert_pattern_to_date(pattern, self.start_date)
        self.save()

    @classmethod
    def advance_todo(cls, todo: "Todo", offset: date = timezone.localdate()) -> "Todo":
        """
        Given a todo item, it will return a new instance of that todo item with start and due date shifted.

        If recurrence is defined as a strict rule, it will be calculated based on the due date or the offset date if no due date is specified.
        If no recurrence is set, this will trigger an error.
        """
        new_todo = Todo(description=todo.description, priority=todo.priority, recurrence=todo.recurrence)
        pattern = todo.recurrence
        strict = False

        if todo.recurrence is None:
            raise NoRecurrenceException()

        if pattern is None or pattern == "":
            raise NoRecurrenceException()

        if pattern.startswith("+"):
            strict = True
            pattern = pattern[1:]

        if strict:
            offset = todo.due_date or offset

        length = todo.length
        new_due_date = convert_pattern_to_date(pattern, offset)

        if not new_due_date:
            raise NoRecurrenceException()

        new_todo.due_date = new_due_date

        if todo.start_date:
            new_start_date = new_due_date - relativedelta(days=length)
            new_todo.start_date = new_start_date

        return new_todo

        """ pattern = todo.recurrence

    if pattern is None or pattern == "":
        raise AttributeError

    if pattern.startswith("+"):
        strict = True
        pattern = pattern[1:]

    if strict:
        offset = todo.due_date or offset or timezone.localdate()
    else:
        offset = offset or timezone.localdate()

    # Calculate the duration of a given todo
    start = todo.start_date or todo.created
    due = todo.due_date
    duration = 0

    if start and due and start < due:
        duration = due - start
        duration = duration.days

    new_due_date = convert_pattern_to_date(pattern, offset)

    new_start_date = None
    if todo.start_date is not None:
        new_start_date = new_due_date - relativedelta(days=duration)

    return Todo.objects.create(
        description=todo.description,
        priority=todo.priority,
        recurrence=todo.recurrence,
        start_date=new_start_date,
        due_date=new_due_date,
    )
 """

        raise NotImplementedError


class TodoOld(models.Model):
    """The standard todo model. holds a description of the todo and a number of fields."""

    class DateUnitChoices(models.TextChoices):
        DAY = "d"
        WEEK = "w"
        MONTH = "m"
        YEAR = "y"

    # General attributes of a todo
    description = models.TextField()
    priority = models.CharField(max_length=1, choices={i: i for i in string.ascii_uppercase}, blank=True, help_text="Priority is ordered from high to low (with A being the higgest priority).")

    # Completed and completion date
    completed = models.BooleanField("Completed?", default=False)
    completion_date = models.DateField(blank=True, null=True)

    # Recurrence can be set, in that case an interval and strict interpretation is required
    recurrence_strict_interval = models.BooleanField(
        "Strict recurrence interval?", default=False, help_text="When selected the new due date will be calculated based on the existing due date, otherwise the completion date will be used to calculate the new due date."
    )
    recurrence_interval_number = models.IntegerField("Interval", blank=True, null=True, help_text="The interval used (a whole integer number).")
    recurrence_interval_unit = models.CharField("Interval unit", max_length=1, choices=DateUnitChoices.choices, blank=True, help_text="The unit for the selected interval: day, week, month or year.")

    # Optionally a due date and start date can also be set for a given todo
    due_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(
        blank=True,
        null=True,
        help_text="Optional. In case this is set it will be used to hide a todo until it can start. In case of postponing or recurrence this date will also be used to calculate the respective new start date (relevant to the other dates).",
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        # If an item is marked as completed and if we have a recurrence tagged to, create a new todo (or verify if it not already exists)
        if self.completed:
            if self.completion_date is None or self.completion_date == "":
                self.completion_date = timezone.localdate()

            if self.recurrence_interval_number is not None and self.recurrence_interval_number != "" and self.recurrence_interval_number != 0:
                interval = None

                match self.recurrence_interval_unit:
                    case Todo.DateUnitChoices.DAY:
                        interval = relativedelta(days=self.recurrence_interval_number)

                    case Todo.DateUnitChoices.WEEK:
                        interval = relativedelta(weeks=self.recurrence_interval_number)

                    case Todo.DateUnitChoices.MONTH:
                        interval = relativedelta(months=self.recurrence_interval_number)

                    case Todo.DateUnitChoices.YEAR:
                        interval = relativedelta(years=self.recurrence_interval_number)

                    case _:
                        # If empty, we assume it's days.
                        interval = relativedelta(days=self.recurrence_interval_number)

                new_due_date = None
                if self.due_date:
                    new_due_date = self.due_date + interval if self.recurrence_strict_interval else self.completion_date + interval

                new_start_date = None
                if self.start_date:
                    start_date_interval = self.due_date - self.start_date
                    new_start_date = new_due_date - start_date_interval if new_due_date is not None else self.completion_date + interval

                Todo.objects.create(
                    description=self.description,
                    priority=self.priority,
                    recurrence_strict_interval=self.recurrence_strict_interval,
                    recurrence_interval_number=self.recurrence_interval_number,
                    recurrence_interval_unit=self.recurrence_interval_unit,
                    due_date=new_due_date,
                    start_date=new_start_date,
                )

        super(Todo, self).save(*args, **kwargs)

    def postpone(self, interval: str | int, unit=DateUnitChoices.DAY) -> None:
        """
        Will postpone the todo by the given interval and unit (default assumes the interval is given in days). To substract, mark the interval as '-' (e.g., -2). Following rules are taken into account:
            - If a due_date exists: new due_date = old due_date + interval
            - If a start_date exists: new start_date = old start_date + interval
            - If there is no start_date: a new start_date will be created equal to today + interval
        """

        # Check to see if the interval starts with a "+" or a "-", if nothing, we assume it's "+"
        if type(interval) is int:
            interval = str(interval)

        if not interval.startswith("-") and not interval.startswith("+"):
            interval = int("+{interval}".format(interval=interval))

        match unit:
            case Todo.DateUnitChoices.DAY:
                interval = relativedelta(days=interval)

            case Todo.DateUnitChoices.WEEK:
                interval = relativedelta(weeks=interval)

            case Todo.DateUnitChoices.MONTH:
                interval = relativedelta(months=interval)

            case Todo.DateUnitChoices.YEAR:
                interval = relativedelta(years=interval)

            case _:
                raise NotImplementedError

        # Postpone will extend both the due_date and start_date if set, if not set it will create a start_date but never a due_date
        if self.due_date is not None:
            self.due_date = self.due_date + interval

        if self.start_date is not None:
            self.start_date = self.start_date + interval
        else:
            self.start_date = timezone.localdate() + interval

    @classmethod
    def advance_todo(cls, todo: Todo, offset: date = timezone.localdate()) -> Todo:
        raise NotImplementedError
