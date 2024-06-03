from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.utils import timezone

from ..models import Todo


class TodoTestCase(TestCase):
    def testRecurrenceDay(self):
        today = timezone.localdate()

        # Test with and without due date
        todo_with_due_date = Todo.objects.create(description="testRecurrenceDay todo with due date", due_date=today + relativedelta(days=+5), recurrence="1d")
        todo_without_due_date = Todo.objects.create(description="testRecurrenceDay todo without due date", recurrence="1d")

        # If we test this with completion_date = due_date there would be no difference from using recurrence_strict=True, so we mark them completed one day later than today
        todo_with_due_date.completed = True
        todo_with_due_date.completion_date = today + relativedelta(days=+1)
        todo_with_due_date.save()

        todo_without_due_date.completed = True
        todo_without_due_date.completion_date = today + relativedelta(days=+1)
        todo_without_due_date.save()

        new_todo_with_due_date = Todo.objects.filter(description=todo_with_due_date.description).last()
        new_todo_without_due_date = Todo.objects.filter(description=todo_without_due_date.description).last()

        self.assertFalse(new_todo_with_due_date.completed)
        self.assertIsNone(new_todo_with_due_date.completion_date)
        self.assertEqual(todo_with_due_date.completion_date, today + relativedelta(days=+1))
        self.assertEqual(new_todo_with_due_date.due_date, todo_with_due_date.completion_date + relativedelta(days=+1))

        self.assertFalse(new_todo_without_due_date.completed)
        self.assertIsNone(new_todo_without_due_date.completion_date)
        self.assertEqual(todo_without_due_date.completion_date, today + relativedelta(days=+1))
        self.assertIsNone(todo_without_due_date.start_date)
        self.assertEqual(new_todo_without_due_date.start_date, todo_without_due_date.completion_date + relativedelta(days=+1))
        self.assertIsNone(new_todo_without_due_date.due_date)

    def testRecurrenceWeek(self):
        today = timezone.localdate()

        # Test with and without due date
        todo_with_due_date = Todo.objects.create(description="testRecurrenceWeek todo with due date", due_date=today + relativedelta(days=+5), recurrence="1w")
        todo_without_due_date = Todo.objects.create(description="testRecurrenceWeek todo without due date", recurrence="1w")

        # If we test this with completion_date = due_date there would be no difference from using recurrence_strict=True, so we mark them completed one day later than today
        todo_with_due_date.completed = True
        todo_with_due_date.completion_date = today + relativedelta(days=+1)
        todo_with_due_date.save()

        todo_without_due_date.completed = True
        todo_without_due_date.completion_date = today + relativedelta(days=+1)
        todo_without_due_date.save()

        new_todo_with_due_date = Todo.objects.filter(description=todo_with_due_date.description).last()
        new_todo_without_due_date = Todo.objects.filter(description=todo_without_due_date.description).last()

        self.assertFalse(new_todo_with_due_date.completed)
        self.assertIsNone(new_todo_with_due_date.completion_date)
        self.assertEqual(todo_with_due_date.completion_date, today + relativedelta(days=+1))
        self.assertEqual(new_todo_with_due_date.due_date, todo_with_due_date.completion_date + relativedelta(weeks=+1))

        self.assertFalse(new_todo_without_due_date.completed)
        self.assertIsNone(new_todo_without_due_date.completion_date)
        self.assertEqual(todo_without_due_date.completion_date, today + relativedelta(days=+1))
        self.assertIsNone(todo_without_due_date.start_date)
        self.assertEqual(new_todo_without_due_date.start_date, todo_without_due_date.completion_date + relativedelta(weeks=+1))
        self.assertIsNone(new_todo_without_due_date.due_date)

    def testRecurrenceMonth(self):
        today = timezone.localdate()

        # Test with and without due date
        todo_with_due_date = Todo.objects.create(description="testRecurrenceWeek todo with due date", due_date=today + relativedelta(days=+5), recurrence="1m")
        todo_without_due_date = Todo.objects.create(description="testRecurrenceWeek todo without due date", recurrence="1m")

        # If we test this with completion_date = due_date there would be no difference from using recurrence_strict=True, so we mark them completed one day later than today
        todo_with_due_date.completed = True
        todo_with_due_date.completion_date = today + relativedelta(days=+1)
        todo_with_due_date.save()

        todo_without_due_date.completed = True
        todo_without_due_date.completion_date = today + relativedelta(days=+1)
        todo_without_due_date.save()

        new_todo_with_due_date = Todo.objects.filter(description=todo_with_due_date.description).last()
        new_todo_without_due_date = Todo.objects.filter(description=todo_without_due_date.description).last()

        self.assertFalse(new_todo_with_due_date.completed)
        self.assertIsNone(new_todo_with_due_date.completion_date)
        self.assertEqual(todo_with_due_date.completion_date, today + relativedelta(days=+1))
        self.assertEqual(new_todo_with_due_date.due_date, todo_with_due_date.completion_date + relativedelta(months=+1))

        self.assertFalse(new_todo_without_due_date.completed)
        self.assertIsNone(new_todo_without_due_date.completion_date)
        self.assertEqual(todo_without_due_date.completion_date, today + relativedelta(days=+1))
        self.assertIsNone(todo_without_due_date.start_date)
        self.assertEqual(new_todo_without_due_date.start_date, todo_without_due_date.completion_date + relativedelta(months=+1))
        self.assertIsNone(new_todo_without_due_date.due_date)

    def testRecurrenceYear(self):
        today = timezone.localdate()

        # Test with and without due date
        todo_with_due_date = Todo.objects.create(description="testRecurrenceYear todo with due date", due_date=today + relativedelta(days=+5), recurrence="1y")
        todo_without_due_date = Todo.objects.create(description="testRecurrenceYear todo without due date", recurrence="1y")

        # If we test this with completion_date = due_date there would be no difference from using recurrence_strict=True, so we mark them completed one day later than today
        todo_with_due_date.completed = True
        todo_with_due_date.completion_date = today + relativedelta(days=+1)
        todo_with_due_date.save()

        todo_without_due_date.completed = True
        todo_without_due_date.completion_date = today + relativedelta(days=+1)
        todo_without_due_date.save()

        new_todo_with_due_date = Todo.objects.filter(description=todo_with_due_date.description).last()
        new_todo_without_due_date = Todo.objects.filter(description=todo_without_due_date.description).last()

        self.assertFalse(new_todo_with_due_date.completed)
        self.assertIsNone(new_todo_with_due_date.completion_date)
        self.assertEqual(todo_with_due_date.completion_date, today + relativedelta(days=+1))
        self.assertEqual(new_todo_with_due_date.due_date, todo_with_due_date.completion_date + relativedelta(years=+1))

        self.assertFalse(new_todo_without_due_date.completed)
        self.assertIsNone(new_todo_without_due_date.completion_date)
        self.assertEqual(todo_without_due_date.completion_date, today + relativedelta(days=+1))
        self.assertIsNone(todo_without_due_date.start_date)
        self.assertEqual(new_todo_without_due_date.start_date, todo_without_due_date.completion_date + relativedelta(years=+1))
        self.assertIsNone(new_todo_without_due_date.due_date)

    def testRecurrenceStrictDay(self):
        today = timezone.localdate()

        # Test with and without due date
        todo_with_due_date = Todo.objects.create(description="testRecurrenceStrictDay todo with due date", due_date=today + relativedelta(days=+5), recurrence="+1d")
        todo_without_due_date = Todo.objects.create(description="testRecurrenceStrictDay todo without due date", recurrence="+1d")

        todo_with_due_date.completed = True
        todo_with_due_date.completion_date = today + relativedelta(days=+1)
        todo_with_due_date.save()

        todo_without_due_date.completed = True
        todo_without_due_date.completion_date = today + relativedelta(days=+1)
        todo_without_due_date.save()

        new_todo_with_due_date = Todo.objects.filter(description=todo_with_due_date.description).last()
        new_todo_without_due_date = Todo.objects.filter(description=todo_without_due_date.description).last()

        self.assertFalse(new_todo_with_due_date.completed)
        self.assertTrue(new_todo_with_due_date.recurrence_strict_interval)
        self.assertIsNone(new_todo_with_due_date.completion_date)
        self.assertEqual(todo_with_due_date.completion_date, today + relativedelta(days=+1))
        self.assertEqual(new_todo_with_due_date.due_date, todo_with_due_date.due_date + relativedelta(days=+1))

        self.assertFalse(new_todo_without_due_date.completed)
        self.assertTrue(new_todo_without_due_date.recurrence_strict_interval)
        self.assertIsNone(new_todo_without_due_date.completion_date)
        self.assertEqual(todo_without_due_date.completion_date, today + relativedelta(days=+1))
        self.assertIsNone(todo_without_due_date.start_date)
        self.assertEqual(new_todo_without_due_date.start_date, todo_without_due_date.due_date + relativedelta(days=+1))
        self.assertIsNone(new_todo_without_due_date.due_date)

    def testRecurrenceStrictWeek(self):
        today = timezone.localdate()

        # Test with and without due date
        todo_with_due_date = Todo.objects.create(description="testRecurrenceStrictWeek todo with due date", due_date=today + relativedelta(days=+5), recurrence="+1w")
        todo_without_due_date = Todo.objects.create(description="testRecurrenceStrictWeek todo without due date", recurrence="+1w")

        todo_with_due_date.completed = True
        todo_with_due_date.completion_date = today + relativedelta(days=+1)
        todo_with_due_date.save()

        todo_without_due_date.completed = True
        todo_without_due_date.completion_date = today + relativedelta(days=+1)
        todo_without_due_date.save()

        new_todo_with_due_date = Todo.objects.filter(description=todo_with_due_date.description).last()
        new_todo_without_due_date = Todo.objects.filter(description=todo_without_due_date.description).last()

        self.assertFalse(new_todo_with_due_date.completed)
        self.assertTrue(new_todo_with_due_date.recurrence_strict_interval)
        self.assertIsNone(new_todo_with_due_date.completion_date)
        self.assertEqual(todo_with_due_date.completion_date, today + relativedelta(days=+1))
        self.assertEqual(new_todo_with_due_date.due_date, todo_with_due_date.due_date + relativedelta(weeks=+1))

        self.assertFalse(new_todo_without_due_date.completed)
        self.assertTrue(new_todo_without_due_date.recurrence_strict_interval)
        self.assertIsNone(new_todo_without_due_date.completion_date)
        self.assertEqual(todo_without_due_date.completion_date, today + relativedelta(days=+1))
        self.assertIsNone(todo_without_due_date.start_date)
        self.assertEqual(new_todo_without_due_date.start_date, todo_without_due_date.due_date + relativedelta(weeks=+1))
        self.assertIsNone(new_todo_without_due_date.due_date)

    def testRecurrenceStrictMonth(self):
        today = timezone.localdate()

        # Test with and without due date
        todo_with_due_date = Todo.objects.create(description="testRecurrenceStrictMonth todo with due date", due_date=today + relativedelta(days=+5), recurrence="+1m")
        todo_without_due_date = Todo.objects.create(description="testRecurrenceStrictMonth todo without due date", recurrence="+1m")

        todo_with_due_date.completed = True
        todo_with_due_date.completion_date = today + relativedelta(days=+1)
        todo_with_due_date.save()

        todo_without_due_date.completed = True
        todo_without_due_date.completion_date = today + relativedelta(days=+1)
        todo_without_due_date.save()

        new_todo_with_due_date = Todo.objects.filter(description=todo_with_due_date.description).last()
        new_todo_without_due_date = Todo.objects.filter(description=todo_without_due_date.description).last()

        self.assertFalse(new_todo_with_due_date.completed)
        self.assertTrue(new_todo_with_due_date.recurrence_strict_interval)
        self.assertIsNone(new_todo_with_due_date.completion_date)
        self.assertEqual(todo_with_due_date.completion_date, today + relativedelta(days=+1))
        self.assertEqual(new_todo_with_due_date.due_date, todo_with_due_date.due_date + relativedelta(months=+1))

        self.assertFalse(new_todo_without_due_date.completed)
        self.assertTrue(new_todo_without_due_date.recurrence_strict_interval)
        self.assertIsNone(new_todo_without_due_date.completion_date)
        self.assertEqual(todo_without_due_date.completion_date, today + relativedelta(days=+1))
        self.assertIsNone(todo_without_due_date.start_date)
        self.assertEqual(new_todo_without_due_date.start_date, todo_without_due_date.due_date + relativedelta(months=+1))
        self.assertIsNone(new_todo_without_due_date.due_date)

    def testRecurrenceStrictYear(self):
        today = timezone.localdate()

        # Test with and without due date
        todo_with_due_date = Todo.objects.create(description="testRecurrenceStrictYear todo with due date", due_date=today + relativedelta(days=+5), recurrence="+1y")
        todo_without_due_date = Todo.objects.create(description="testRecurrenceStrictYear todo without due date", recurrence="+1y")

        todo_with_due_date.completed = True
        todo_with_due_date.completion_date = today + relativedelta(days=+1)
        todo_with_due_date.save()

        todo_without_due_date.completed = True
        todo_without_due_date.completion_date = today + relativedelta(days=+1)
        todo_without_due_date.save()

        new_todo_with_due_date = Todo.objects.filter(description=todo_with_due_date.description).last()
        new_todo_without_due_date = Todo.objects.filter(description=todo_without_due_date.description).last()

        self.assertFalse(new_todo_with_due_date.completed)
        self.assertTrue(new_todo_with_due_date.recurrence_strict_interval)
        self.assertIsNone(new_todo_with_due_date.completion_date)
        self.assertEqual(todo_with_due_date.completion_date, today + relativedelta(days=+1))
        self.assertEqual(new_todo_with_due_date.due_date, todo_with_due_date.due_date + relativedelta(years=+1))

        self.assertFalse(new_todo_without_due_date.completed)
        self.assertTrue(new_todo_without_due_date.recurrence_strict_interval)
        self.assertIsNone(new_todo_without_due_date.completion_date)
        self.assertEqual(todo_without_due_date.completion_date, today + relativedelta(days=+1))
        self.assertIsNone(todo_without_due_date.start_date)
        self.assertEqual(new_todo_without_due_date.start_date, todo_without_due_date.due_date + relativedelta(years=+1))
        self.assertIsNone(new_todo_without_due_date.due_date)

    def testRecurrenceWithStartDateAndNoDueDate(self):
        today = timezone.localdate()

        todo_with_start_date = Todo.objects.create(description="testRecurrenceWithStartDateAndNoDueDate without strict date", recurrence="1w")
        todo_with_strict_start_date = Todo.objects.create(description="testRecurrenceWithStartDateAndNoDueDate with strict date", recurrence="+1w", start_date=today)

        todo_with_start_date.completed = True
        todo_with_start_date.completion_date = today + relativedelta(days=+1)
        todo_with_start_date.save()

        todo_with_strict_start_date.completed = True
        todo_with_strict_start_date.completion_date = today + relativedelta(days=+1)
        todo_with_strict_start_date.save()

        new_todo_with_start_date = Todo.objects.filter(description=todo_with_start_date).last()
        new_todo_with_strict_start_date = Todo.objects.filter(description=todo_with_strict_start_date.description).last()

        self.assertFalse(new_todo_with_start_date.completed)
        self.assertIsNone(new_todo_with_start_date.completion_date)
        self.assertEqual(todo_with_start_date.completion_date, today + relativedelta(days=+1))
        self.assertEqual(new_todo_with_start_date.start_date, todo_with_start_date.completion_date + relativedelta(weeks=+1))

        self.assertFalse(new_todo_with_strict_start_date.completed)
        self.assertTrue(new_todo_with_strict_start_date.recurrence_strict_interval)
        self.assertIsNone(new_todo_with_strict_start_date.completion_date)
        self.assertEqual(todo_with_strict_start_date.completion_date, today + relativedelta(days=+1))
        self.assertEqual(new_todo_with_strict_start_date.start_date, todo_with_strict_start_date.start_date + relativedelta(weeks=+1))

    def testRecurrenceWithStartDateAndDueDate(self):
        today = timezone.localdate()

        todo_with_start_date = Todo.objects.create(description="testRecurrenceWithStartDateAndDueDate without strict date", recurrence="1w", start_date=today, due_date=today + relativedelta(days=+2))
        todo_with_strict_start_date = Todo.objects.create(description="testRecurrenceWithStartDateAndDueDate with strict date", recurrence="+1w", start_date=today, due_date=today + relativedelta(days=+2))

        todo_with_start_date.completed = True
        todo_with_start_date.completion_date = today + relativedelta(days=+1)
        todo_with_start_date.save()

        todo_with_strict_start_date.completed = True
        todo_with_strict_start_date.completion_date = today + relativedelta(days=+1)
        todo_with_strict_start_date.save()

        new_todo_with_start_date = Todo.objects.filter(description=todo_with_start_date).last()
        new_todo_with_strict_start_date = Todo.objects.filter(description=todo_with_strict_start_date.description).last()

        self.assertFalse(new_todo_with_start_date.completed)
        self.assertIsNone(new_todo_with_start_date.completion_date)
        self.assertEqual(todo_with_start_date.completion_date, today + relativedelta(days=+1))
        self.assertEqual(new_todo_with_start_date.start_date, todo_with_start_date.completion_date + relativedelta(weeks=+1) + relativedelta(days=-2))

        self.assertFalse(new_todo_with_strict_start_date.completed)
        self.assertTrue(new_todo_with_strict_start_date.recurrence_strict_interval)
        self.assertIsNone(new_todo_with_strict_start_date.completion_date)
        self.assertEqual(todo_with_strict_start_date.completion_date, today + relativedelta(days=+1))
        self.assertEqual(new_todo_with_strict_start_date.start_date, todo_with_strict_start_date.due_date + relativedelta(weeks=+1) + relativedelta(days=-2))

    def testPostpone(self):
        today = timezone.localdate()

        # Test with and without due date
        todo_with_due_date = Todo.objects.create(description="Test todo with due date", due_date=today + relativedelta(days=+5))
        todo_without_due_date = Todo.objects.create(description="Test todo without due date")

        todo_with_due_date.postpone(interval="5d")
        self.assertEqual(todo_with_due_date.due_date, today + relativedelta(days=+10))
        self.assertEqual(todo_with_due_date.start_date, today + relativedelta(days=+5))

        todo_without_due_date.postpone(interval="5d")
        self.assertIsNone(todo_without_due_date.due_date)
        self.assertEqual(todo_without_due_date.start_date, today + relativedelta(days=+5))

    def testPostponeWithStartDate(self):
        today = timezone.localdate()

        # Test with and without due date
        todo_with_due_date = Todo.objects.create(description="Test todo with due date", due_date=today + relativedelta(days=+5), start_date=today + relativedelta(days=+1))
        todo_without_due_date = Todo.objects.create(description="Test todo without due date", start_date=today + relativedelta(days=+1))

        todo_with_due_date.postpone(interval="5d")
        self.assertEqual(todo_with_due_date.due_date, today + relativedelta(days=+10))
        self.assertEqual(todo_with_due_date.start_date, today + relativedelta(days=+6))

        todo_without_due_date.postpone(interval="5d")
        self.assertIsNone(todo_without_due_date.due_date)
        self.assertEqual(todo_without_due_date.start_date, today + relativedelta(days=+6))
