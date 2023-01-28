from django.test import TestCase
from django.urls import reverse
from datetime import datetime

from todo_app.models.todo_list import TodoList


class TodoViewTests(TestCase):
    def setUp(self):
        self.form_data = {"task": "Test task"}
        self.response = self.client.post(reverse("add_todo_item"), data=self.form_data)

    def test_create_todo_item(self):
        self.assertEqual(TodoList.objects.count(), 1)
        todo_item = TodoList.objects.first()
        self.assertEqual(todo_item.task, "Test task")
        self.assertEqual(todo_item.completed, False)
        self.assertIsInstance(todo_item.created_at, datetime)

    def test_add_todo_item_view(self):
        self.assertEqual(self.response.status_code, 302)
        self.assertRedirects(self.response, reverse("todo_list"))

    def test_todo_list_view(self):
        response = self.client.get(reverse("todo_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test task")
        self.assertTemplateUsed(response, "todo_list.html")

    def test_remove_todo_item_view(self):
        todo_item = TodoList.objects.first()
        response = self.client.post(
            reverse("remove_todo_item", kwargs={"pk": todo_item.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("todo_list"))
        self.assertEqual(TodoList.objects.count(), 0)

    def test_update_todo_item_view(self):
        todo_item = TodoList.objects.first()
        response = self.client.post(
            reverse("update_todo_item", kwargs={"pk": todo_item.pk}),
            data={"completed": "on"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("todo_list"))
        todo_item.refresh_from_db()
        self.assertTrue(todo_item.completed)
