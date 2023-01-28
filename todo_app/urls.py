"""todo_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from todo_app.views.home_view import home
from todo_app.views.todo_list_view import (
    todo_list,
    add_todo_item,
    remove_todo_item,
    update_todo_item,
)

urlpatterns = [
    path("", home, name="home"),
    path("todo/", todo_list, name="todo_list"),
    path("add/", add_todo_item, name="add_todo_item"),
    path("remove_todo_item/<int:pk>/", remove_todo_item, name="remove_todo_item"),
    path("update_todo_item/<int:pk>/", update_todo_item, name="update_todo_item"),
]
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()
