from django.shortcuts import render

from todo_app.forms.todo_form import TodoForm
from todo_app.models.todo_list import TodoList
from django.shortcuts import render, redirect
from django.urls import reverse


def add_todo_item(request):
    if request.method == "POST":
        task_description = request.POST["task_description"]
        new_task = TodoList(description=task_description)
        new_task.save()
        return redirect(reverse("todo_list"))


def todo_list(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            TodoList.objects.create(task=form.cleaned_data["task"])
            return redirect("todo_list")
    else:
        form = TodoForm()
    todo_items = TodoList.objects.all()
    return render(request, "todo_list.html", {"todo_items": todo_items, "form": form})
