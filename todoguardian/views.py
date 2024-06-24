from django.contrib import messages
from django.db.models import F, Value
from django.db.models.fields import DateField
from django.db.models.functions import Coalesce
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from .functions.recurrence import NoRecurrenceException, advance_todo
from .models import Todo


def dashboard(request: HttpRequest) -> HttpResponse:
    todos = (
        Todo.objects.filter(completion_date=None)
        .exclude(start_date__gt=timezone.localdate())
        .annotate(due_date_value=Coalesce("due_date", Value("9999-12-31"), output_field=DateField()), start_date_value=Coalesce("start_date", Value("9999-12-31"), output_field=DateField()))
        .order_by("due_date_value", "start_date_value", "priority")
        .prefetch_related("projects", "contexts", "annotations")
    )

    return render(request, "dashboard.html", {"todos": todos})


def add(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        todo = Todo.from_string(request.POST.get("todo_string"))
        messages.success(request, "New todo <span class='font-semibold'>{description}</span> created".format(description=todo.description))

    return redirect("todoguardian:dashboard")


def edit(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == "POST":
        todo = Todo.objects.get(id=id)
        todo.update_from_string(request.POST.get("todo_string"))
        messages.success(request, "Todo <span class='font-semibold'>{description}</span> changed".format(description=todo.description))

    return redirect("todoguardian:dashboard")


def postpone(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == "POST":
        todo = Todo.objects.get(id=id)
        todo.postpone(request.POST.get("pattern"))
        messages.success(request, "Todo <span class='font-semibold'>{description}</span> postponed to new due date: {due_date}".format(description=todo.description, due_date=todo.due_date.strftime("%a %d.%m.%y")))

    return redirect("todoguardian:dashboard")


def annotate(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == "POST":
        todo = Todo.objects.get(id=id)
        todo.annotations.create(text=request.POST.get("annotation"))
        messages.success(request, "Annotation added to <span class='font-semibold'>{description}</span>".format(description=todo.description))

    return redirect("todoguardian:dashboard")


def complete(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        todo = Todo.objects.get(id=request.POST.get("todo_id"))

        if todo.is_completed:
            todo.mark_not_complete()
            messages.success(request, "Todo <span class='font-semibold'>{description}</span> marked as not completed".format(description=todo.description))

        else:
            todo.mark_complete()

            try:
                advance_todo(todo)
                messages.success(request, "Todo <span class='font-semibold'>{description}</span> marked as completed".format(description=todo.description))
                messages.success(request, "New todo <span class='font-semibold'>{description}</span> created".format(description=todo.description))

            except NoRecurrenceException:
                messages.success(request, "Todo <span class='font-semibold'>{description}</span> marked as completed".format(description=todo.description))

    return redirect("todoguardian:dashboard")
