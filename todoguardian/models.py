from django.db import models
import string
from dateutil.relativedelta import relativedelta
from django.utils import timezone, text


class Todo(models.Model):
    """This class contains common fields for storing todos"""

    description = models.TextField()
    priority = models.CharField(max_length=1, choices={i: i for i in string.ascii_uppercase}, blank=True)
    completed = models.BooleanField(default=False)
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
