from django.urls import path

from . import views

app_name = "todoguardian"
urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name="add_todo"),
    path("edit/<int:id>/", views.edit, name="edit_todo"),
    path("notes/", views.notes, name="notes"),
    path("complete/", views.complete, name="complete"),
    path("postpone/", views.postpone, name="postpone"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add/", views.add, name="add"),  # keep in to make old version work
    path("edit/", views.edit, name="edit"),  # keep in to make old version work
]
