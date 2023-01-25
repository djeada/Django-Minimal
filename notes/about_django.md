## What is Django?
Django is a high-level Python web framework that enables developers to build robust and powerful web applications quickly and easily. It follows the Model-View-Controller (MVC) architectural pattern and encourages the use of reusable code.

## Getting Started

To start a new Django project, you will first need to install Django on your machine. This can be done using pip, the package installer for Python, by running the command `pip install Django`.

Once Django is installed, you can create a new project using the command `django-admin startproject project_name`. This will create a new directory with the same name as the project, containing the basic project structure and settings.

To create a database for your project, you can use the command `python manage.py makemigrations` followed by `python manage.py migrate` to create the necessary tables.

You can then start the development server by running `python manage.py runserver` and view your project by navigating to `http://localhost:8000/` in your web browser.

## Models

Models in Django are used to define the data structure of your application. They are defined as Python classes that inherit from the django.db.models.Model class and use fields such as CharField, IntegerField, and DateTimeField to specify the data types and attributes of the fields.

For example, a model for a blog post might look like this:

```python
from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
```

In this example, the BlogPost model has three fields: title, content, and created_at. The auto_now_add and auto_now attributes on the created_at and updated_at fields respectively ensure that the fields are automatically set to the current date and time when a new object is created or an existing object is updated.

## URLs and Views

Django uses a URL dispatcher to map URLs to views, which are responsible for handling requests and returning responses. The project's urls.py file is used to define the URLs for the entire project, while each app has its own urls.py file for defining the URLs for that app.

For example, the urls.py file for an app called blog might look like this:

```python
from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>/', views.detail, name='detail'),
]
```

This file maps the root URL (/) to the index view and the /<int:post_id>/ URL to the detail view. The path function takes the URL pattern as the first argument and the view function as the second argument.

Views are defined in the views.py file of each app, and are typically responsible for processing the request, interacting with the model, and returning a response.

For example, the index view for the blog app might look like this:

```python
from django.shortcuts import render
from .models import BlogPost

def index(request):
    latest_posts = BlogPost.objects.order_by('-created_at')[:5]
    context = {'latest_posts': latest_posts}
    return render(request, 'blog/index.html', context)
```

## Templates

Django uses templates to separate the presentation logic from the views. Templates are written in a special language called Django template language (DTL) which allows you to define the structure and layout of a page, and insert data retrieved from the view.

For example, the index.html template for the blog app might look like this:

```html
<h1>Latest Posts</h1>
<ul>
{% for post in latest_posts %}
    <li>{{ post.title }}</li>
{% endfor %}
</ul>
```

This template uses DTL to iterate over the latest_posts variable passed from the view, and display the title of each post in an unordered list.

### Template Inheritance

Django also supports template inheritance, which allows you to define a base template containing the common elements of your site (such as the header, footer, and navigation), and then extend that template in other templates to add unique content. This allows you to keep your code DRY (Don't Repeat Yourself) and make global changes to the site's layout more easily.

For example, you might have a base.html template that looks like this:

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Default Title{% endblock %}</title>
</head>
<body>
    <header>
        <nav>
            <a href="{% url 'index' %}">Home</a>
        </nav>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer>
        Copyright ©2022
    </footer>
</body>
</html>
```

And then extend this template in the index.html template:

```html
{% extends 'base.html' %}

{% block title %}Latest Posts{% endblock %}

{% block content %}
<h1>Latest Posts</h1>
<ul>
{% for post in latest_posts %}
    <li>{{ post.title }}</li>
{% endfor %}
</ul>
{% endblock %}
```

In this way, you can define the common elements of your site in a single template and reuse them in other templates.

