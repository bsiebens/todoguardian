from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.utils import timezone

from ..models import Todo


class TodoTestCase(TestCase):
    def setUp(self):
        super().setUp()

        self.bare_todo = Todo.objects.create(description="Bare Todo")
        self.todo_with_due = Todo.objects.create(description="Todo with due date", due_date=timezone.localdate() + relativedelta(days=5))
        self.todo_with_start = Todo.objects.create(description="Todo with due date", start_date=timezone.localdate() + relativedelta(days=1))
        self.recurring_todo = Todo.objects.create(description="Recurring Todo", recurrence="1w")
        self.strict_recurring_todo = Todo.objects.create(description="Strict Recurring Todo", recurrence="+1w")

    def testNotCompleted(self):
        self.assertFalse(self.bare_todo._completed)

    def testCompletedWithDate(self):
        yesterday = timezone.localdate() + relativedelta(days=-1)
        self.bare_todo.complete(yesterday)

        self.assertEqual(self.bare_todo.completion_date, yesterday)
        self.assertTrue(self.bare_todo._completed)

    def testCompletedNoDate(self):
        self.bare_todo.complete()

        self.assertEqual(self.bare_todo.completion_date, timezone.localdate())
        self.assertTrue(self.bare_todo._completed)

    def testPostponeDueDate(self):
        self.todo_with_due.postpone("5d")
        self.assertEqual(self.todo_with_due.due_date, timezone.localdate() + relativedelta(days=10))

    def testPostponeNoStartDate(self):
        self.todo_with_due.postpone("5d")
        self.assertEqual(self.todo_with_due.start_date, timezone.localdate() + relativedelta(days=5))

    def testPostponeStartDate(self):
        self.todo_with_start.postpone("5d")
        self.assertEqual(self.todo_with_start.start_date, timezone.localdate() + relativedelta(days=6))
        self.assertIsNone(self.todo_with_start.due_date)
