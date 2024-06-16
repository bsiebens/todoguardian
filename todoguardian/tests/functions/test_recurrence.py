from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.utils import timezone

from ...exceptions import NoRecurrenceException
from ...functions.recurrence import advance_todo
from ...models import Todo


class TodoTestCase(TestCase):
    def setUp(self):
        super().setUp()

        self.bare_todo = Todo.objects.create(description="Bare Todo")
        self.todo_with_due = Todo.objects.create(description="Todo with due date", due_date=timezone.localdate() + relativedelta(days=5))
        self.todo_with_start = Todo.objects.create(description="Todo with due date", start_date=timezone.localdate() + relativedelta(days=1))
        self.recurring_todo = Todo.objects.create(description="Recurring Todo", recurrence="1w")
        self.strict_recurring_todo = Todo.objects.create(description="Strict Recurring Todo", recurrence="+1w")

    def testRecurrenceDueDateFuture(self):
        new_due_date = timezone.localdate() + relativedelta(days=7)

        self.recurring_todo.due_date = timezone.localdate() + relativedelta(days=1)
        new_todo = advance_todo(self.recurring_todo, offset=timezone.localdate())
        self.assertEqual(new_todo.due_date, new_due_date)

    def testRecurrenceDueDatePast(self):
        new_due_date = timezone.localdate() + relativedelta(days=7)

        self.recurring_todo.due_date = timezone.localdate() + relativedelta(days=-8)
        new_todo = advance_todo(self.recurring_todo, offset=timezone.localdate())
        self.assertEqual(new_todo.due_date, new_due_date)

    def testRecurrenceDueToday(self):
        new_due_date = timezone.localdate() + relativedelta(days=7)

        self.recurring_todo.due_date = timezone.localdate()
        new_todo = advance_todo(self.recurring_todo, offset=timezone.localdate())
        self.assertEqual(new_todo.due_date, new_due_date)

    def testRecurrenceDueDateFutureStrict(self):
        new_due_date = timezone.localdate() + relativedelta(days=8)

        self.strict_recurring_todo.due_date = timezone.localdate() + relativedelta(days=1)
        new_todo = advance_todo(self.strict_recurring_todo, offset=timezone.localdate())
        self.assertEqual(new_todo.due_date, new_due_date)

    def testRecurrenceDueDatePastStrict(self):
        new_due_date = timezone.localdate() + relativedelta(days=-1)

        self.strict_recurring_todo.due_date = timezone.localdate() + relativedelta(days=-8)
        new_todo = advance_todo(self.strict_recurring_todo, offset=timezone.localdate())
        self.assertEqual(new_todo.due_date, new_due_date)

    def testRecurrenceDueTodayStrict(self):
        new_due_date = timezone.localdate() + relativedelta(days=7)

        self.strict_recurring_todo.due_date = timezone.localdate()
        new_todo = advance_todo(self.strict_recurring_todo, offset=timezone.localdate())
        self.assertEqual(new_todo.due_date, new_due_date)

    def testRecurrenceNoDueDate(self):
        new_due = timezone.localdate() + relativedelta(days=7)

        new_todo = advance_todo(self.recurring_todo, offset=timezone.localdate())
        self.assertEqual(new_todo.due_date, new_due)

    def testRecurrenceStrictNoDueDate(self):
        new_due = timezone.localdate() + relativedelta(days=7)

        new_todo = advance_todo(self.strict_recurring_todo, offset=timezone.localdate())
        self.assertEqual(new_todo.due_date, new_due)

    def testRecurrenceStartDayBefore(self):
        self.recurring_todo.start_date = timezone.localdate() + relativedelta(days=-1)
        self.recurring_todo.due_date = timezone.localdate()

        new_start = timezone.localdate() + relativedelta(days=6)
        new_todo = advance_todo(self.recurring_todo, offset=timezone.localdate())
        self.assertEqual(new_todo.start_date, new_start)

    def testRecurrenceStrictStartDayBefore(self):
        self.strict_recurring_todo.start_date = timezone.localdate() + relativedelta(days=-2)
        self.strict_recurring_todo.due_date = timezone.localdate() + relativedelta(days=-1)

        new_start = timezone.localdate() + relativedelta(days=5)
        new_todo = advance_todo(self.strict_recurring_todo, offset=timezone.localdate())
        self.assertEqual(new_todo.start_date, new_start)

    def testRecurrenceStartDayEqualToDueDate(self):
        self.recurring_todo.due_date = timezone.localdate()
        self.recurring_todo.start_date = timezone.localdate()

        new_start = timezone.localdate() + relativedelta(days=7)
        new_todo = advance_todo(self.recurring_todo, offset=timezone.localdate())
        self.assertEqual(new_todo.start_date, new_start)

    def testNoRecurrence(self):
        todo = Todo.objects.create(description="Test description")
        self.assertRaises(NoRecurrenceException, advance_todo, todo)

    def testInvalidRecurrence(self):
        todo = Todo.objects.create(description="Test description", recurrence="1f")
        self.assertRaises(NoRecurrenceException, advance_todo, todo)
