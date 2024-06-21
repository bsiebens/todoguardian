from django.contrib import messages
from django.db.models import F, Value
from django.db.models.fields import DateField
from django.db.models.functions import Coalesce
from django.shortcuts import redirect, render
from django.utils import timezone
from django.http import HttpRequest, HttpResponse

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
        messages.success(request, "Todo '{description}' changed".format(description=todo.description))

    return redirect("todoguardian:dashboard")


def index(request):
    todos = (
        Todo.objects.annotate(
            due_date_value=Coalesce("due_date", Value("9999-12-31"), output_field=DateField()),
            start_date_value=Coalesce("start_date", Value("9999-12-31"), output_field=DateField()),
        )
        .order_by(
            F("_completed"),
            "due_date_value",
            "start_date_value",
            "priority",
        )
        .prefetch_related("projects", "contexts", "annotations")
    )

    return render(request, "index.html", {"todos": todos})


""" def add(request):
    if request.method == "POST":
        todo = Todo.from_string(request.POST.get("addTodoFromString"))
        messages.success(request, "New todo '{description}' created".format(description=todo.description))

    return redirect("todoguardian:index")
 """


def complete(request):
    if request.method == "POST":
        todo = Todo.objects.get(id=request.POST.get("completeTodo"))

        if todo.is_completed:
            todo.mark_not_complete()
            messages.success(request, "Todo '{description}' marked as not completed".format(description=todo.description))

        else:
            todo.mark_complete()

            try:
                advance_todo(todo)
                messages.success(request, "Todo '{description}' marked as completed".format(description=todo.description))
                messages.success(request, "New todo '{description}' created".format(description=todo.description))

            except NoRecurrenceException:
                messages.success(request, "Todo '{description}' marked as completed".format(description=todo.description))

    return redirect("todoguardian:index")


""" def edit(request):
    if request.method == "POST":
        todo = Todo.objects.get(id=request.POST.get("editTodoID"))
        todo.update_from_string(request.POST.get("editTodoString"))
        messages.success(request, "Todo '{description}' changed".format(description=todo.description))

    return redirect("todoguardian:index") """


def postpone(request):
    if request.method == "POST":
        todo = Todo.objects.get(id=request.POST.get("postponeTodoID"))
        todo.postpone(request.POST.get("postponeTodoPattern"))
        messages.success(request, "Todo '{description}' postponed to {date}".format(description=todo.description, date=todo.start_date.strftime("%a %d.%m.%y")))

    return redirect("todoguardian:index")


def notes(request):
    if request.method == "POST":
        todo = Todo.objects.get(id=request.POST.get("noteTodoID"))
        todo.annotations.create(text=request.POST.get("noteTodoText"))
        messages.success(request, "Note added to todo '{description}'".format(description=todo.description))

    return redirect("todoguardian:index")
