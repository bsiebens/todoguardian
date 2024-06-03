from django.db import models
import string
from dateutil.relativedelta import relativedelta
from django.utils import timezone


class Todo(models.Model):
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

    def postpone(self, interval: str | int, unit=DateUnitChoices.DAY) -> None:
        """Will postpone the todo by the given interval and unit (default assumes the interval is given in days). To substract, mark the interval as '-' (e.g., -2)."""

        # Check to see if the interval starts with a "+" or a "-", if nothing, we assume it's "+"
        if type(interval) == int:
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
