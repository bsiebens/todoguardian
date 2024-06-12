from django.shortcuts import render
from .models import Todo


def index(request):
    todos = Todo.objects.all().order_by("-_completed", "due_date", "start_date", "priority").prefetch_related("projects", "contexts")

    return render(request, "index.html", {"todos": todos})
