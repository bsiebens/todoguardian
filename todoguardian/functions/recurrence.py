from datetime import date

from dateutil.relativedelta import relativedelta

from ..exceptions import NoRecurrenceException
from ..models import Todo
from .date import to_date


def advance_todo(todo: Todo, offset: date | None = None, save: bool = True) -> Todo:
    """
    Given a todo item, calculates and creates the next iteration of this todo. Dates will be shifted
    according to the recurrence rule set on the original todo.

    In case the recurrence rule starts with a "+", a strict recurrence is observer, i.e. the new
    dates are caclulated based on the real due date, rather than the supplied offset date.

    In case no due date is given, offset will always be used, which defaults to today.

    In case there is no recurrence rule, this will raise a `NoRecurrenceException`.

    By passing in `save=False` the new todo is only created but not saved to the database.
    """
    advanced_todo = Todo(description=todo.description, priority=todo.priority, recurrence=todo.recurrence)
    pattern = todo.recurrence
    strict = False

    if pattern is None or pattern == "":
        raise NoRecurrenceException()

    if pattern.startswith("+"):
        pattern = pattern[1:]
        strict = True

    if strict:
        if todo.due_date is not None:
            offset = todo.due_date

    # Calculate the new due_date
    due_date = to_date(pattern, offset)
    if due_date is None:
        raise NoRecurrenceException()

    advanced_todo.due_date = due_date

    if todo.start_date:
        advanced_todo.start_date = due_date - relativedelta(days=todo.length)

    if save:
        advanced_todo.save()

    return advanced_todo
