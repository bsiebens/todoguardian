from django.urls import path

from . import views

app_name = "todoguardian"
urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    path("complete/", views.complete, name="complete"),
    path("edit/", views.edit, name="edit"),
    path("postpone/", views.postpone, name="postpone"),
    path("notes/", views.notes, name="notes"),
]
