import datetime

from django.test import TestCase

from todo_app.models.todo_list import TodoList


class TodoListTest(TestCase):
    def test_create_todo_item(self):
        todo_item = TodoList.objects.create(
            task="Test task", completed=False, created_at=datetime.datetime.now()
        )
        self.assertEqual(todo_item.task, "Test task")
        self.assertFalse(todo_item.completed)
        self.assertIsInstance(todo_item.created_at, datetime.datetime)

    def test_str_representation(self):
        todo_item = TodoList.objects.create(
            task="Test task", completed=False, created_at=datetime.datetime.now()
        )
        self.assertEqual(str(todo_item), "Test task")

    def test_default_completed_value(self):
        todo_item = TodoList.objects.create(
            task="Test task", created_at=datetime.datetime.now()
        )
        self.assertFalse(todo_item.completed)
