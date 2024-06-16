from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.utils import timezone

from ..models import Todo, Project, Context


class TodoTestCase(TestCase):
    def setUp(self):
        super().setUp()

        self.bare_todo = Todo.objects.create(description="Bare Todo")
        self.todo_with_due = Todo.objects.create(description="Todo with due date", due_date=timezone.localdate() + relativedelta(days=5))
        self.todo_with_start = Todo.objects.create(description="Todo with due date", start_date=timezone.localdate() + relativedelta(days=1))
        self.recurring_todo = Todo.objects.create(description="Recurring Todo", recurrence="1w")
        self.strict_recurring_todo = Todo.objects.create(description="Strict Recurring Todo", recurrence="+1w")
        self.todo_overdue = Todo.objects.create(description="Todo overdue", due_date=timezone.localdate() + relativedelta(days=-1))
        self.todo_due_today = Todo.objects.create(description="Todo due today", due_date=timezone.localdate())
        self.todo_due_next_3_days = Todo.objects.create(description="Todo due next 3 days", due_date=timezone.localdate() + relativedelta(days=2))
        self.project_a = Project.objects.create(name="projecta")
        self.context_a = Context.objects.create(name="contexta")

    def testNotCompleted(self):
        self.assertFalse(self.bare_todo._completed)

    def testCompletedWithDate(self):
        yesterday = timezone.localdate() + relativedelta(days=-1)
        self.bare_todo.mark_complete(yesterday)

        self.assertEqual(self.bare_todo.completion_date, yesterday)
        self.assertTrue(self.bare_todo._completed)

    def testRevertComplete(self):
        self.bare_todo.mark_complete()
        self.bare_todo.mark_not_complete()

        self.assertIsNone(self.bare_todo.completion_date)
        self.assertFalse(self.bare_todo._completed)

    def testCompletedNoDate(self):
        self.bare_todo.mark_complete()

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

    def testNotOverdue(self):
        self.assertFalse(self.todo_with_due.is_overdue)

    def testOverdue(self):
        self.assertTrue(self.todo_overdue.is_overdue)

    def testDueToday(self):
        self.assertFalse(self.todo_due_today.is_overdue)

    def testDueMoreThan3Days(self):
        self.assertFalse(self.todo_with_due.is_due_soon)

    def testDueLessThan3Days(self):
        self.assertTrue(self.todo_due_next_3_days.is_due_soon)

    def testTodoCreationFromString(self):
        testString = "(A) New todo due:today +project1 +project2 +projecta @context1 @context2 @contexta t:tomorrow rec:+1w"
        todo = Todo.from_string(testString)

        self.assertEqual(todo.priority, "A")
        self.assertEqual(todo.description, "New todo")
        self.assertEqual(todo.due_date, timezone.localdate())
        self.assertEqual(todo.recurrence, "+1w")
        self.assertEqual(todo.start_date, timezone.localdate() + relativedelta(days=1))
        self.assertEqual(todo.projects.all().count(), 3)
        self.assertEqual(todo.contexts.all().count(), 3)
        self.assertEqual(Project.objects.all().count(), 3)
        self.assertEqual(Context.objects.all().count(), 3)

    def testTodoCreationFromStringAbsoluteDate(self):
        testString = "(A) New todo due:{today} +project1 +project2 +projecta @context1 @context2 @contexta t:tomorrow rec:+1w".format(today=timezone.localdate().isoformat())
        todo = Todo.from_string(testString)

        self.assertEqual(todo.priority, "A")
        self.assertEqual(todo.description, "New todo")
        self.assertEqual(todo.due_date, timezone.localdate())
        self.assertEqual(todo.recurrence, "+1w")
        self.assertEqual(todo.start_date, timezone.localdate() + relativedelta(days=1))
        self.assertEqual(todo.projects.all().count(), 3)
        self.assertEqual(todo.contexts.all().count(), 3)
        self.assertEqual(Project.objects.all().count(), 3)
        self.assertEqual(Context.objects.all().count(), 3)
