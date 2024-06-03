from .models import Todo
from .date_functions import convert_pattern_to_date
from datetime import date
from django.utils import timezone
from dateutil.relativedelta import relativedelta


def generate_new_todo(todo: Todo, offset: date | None = None, strict: bool = False) -> Todo:
    """Generates a new todo based on the given todo and it's recurrence pattern."""
    pattern = todo.recurrence

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
