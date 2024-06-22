from django.urls import path

from . import views

app_name = "todoguardian"
urlpatterns = [
    path("", views.dashboard, name="index"),
    path("add/", views.add, name="add_todo"),
    path("edit/<int:id>/", views.edit, name="edit_todo"),
    path("postpone/<int:id>/", views.postpone, name="postpone_todo"),
    path("annotate/<int:id>/", views.annotate, name="annotate_todo"),
    path("complete/", views.complete, name="complete_todo"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
