from django.shortcuts import render, redirect
from django.urls import reverse
from todo_app.forms.todo_form import TodoForm
from todo_app.models.todo_list import TodoList
import datetime

def create_todo_item(form):
    TodoList.objects.create(task=form.cleaned_data["task"], completed=False, created_at=datetime.datetime.now())

def add_todo_item(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            create_todo_item(form)
            return redirect(reverse('todo_list'))
    else:
        form = TodoForm()
    return render(request, "todo_form.html", {"form": form})

def todo_list(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            create_todo_item(form)
    else:
        form = TodoForm()

    todo_items = TodoList.objects.all()    
    return render(request, "todo_list.html", {"todo_items": todo_items, "form": form})

def remove_todo_item(request, pk):
    task = TodoList.objects.get(pk=pk)
    task.save()
    return redirect('todo_list')

def update_todo_item(request, pk):
    task = TodoList.objects.get(pk=pk)
    task.completed = request.POST.get("completed") == "on"
    task.save()
    return redirect("todo_list")
