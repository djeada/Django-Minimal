from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from todo_app.forms.todo_form import TodoForm
from todo_app.models.todo_list import TodoList
import datetime


def create_todo_item(form: TodoForm) -> None:
    """
    Create a TodoList object from the given form.

    :param form: the TodoForm containing the task
    """
    TodoList.objects.create(
        task=form.cleaned_data["task"],
        completed=False,
        created_at=datetime.datetime.now(),
    )


def add_todo_item(request: HttpRequest) -> HttpResponse:
    """
    Handle the form submission for creating a new TodoList item.

    :param request: the request object
    :return: a redirect to the TodoList view or the TodoForm view with form errors
    """
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            create_todo_item(form)
            return redirect(reverse("todo_list"))
    else:
        form = TodoForm()
    return render(request, "todo_form.html", {"form": form})


def todo_list(request: HttpRequest) -> HttpResponse:
    """
    Render the TodoList view.

    :param request: the request object
    :return: the rendered TodoList view
    """
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            create_todo_item(form)
    else:
        form = TodoForm()

    todo_items = TodoList.objects.all()
    return render(request, "todo_list.html", {"todo_items": todo_items, "form": form})


def remove_todo_item(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Remove the TodoList item with the given primary key.

    :param request: the request object
    :param pk: the primary key of the TodoList item to remove
    :return: a redirect to the TodoList view
    """
    TodoList.objects.filter(id=pk).delete()
    return redirect(reverse("todo_list"))


def update_todo_item(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Update the completed status of the TodoList item with the given primary key.

    :param request: the request object
    :param pk: the primary key of the TodoList item to update
    :return: a redirect to the TodoList view
    """
    task = TodoList.objects.get(pk=pk)
    task.completed = request.POST.get("completed") == "on"
    task.save()
    return redirect("todo_list")
