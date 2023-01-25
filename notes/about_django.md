
## What is Django?
Django is a web framework which helps you build
interactive websites using Python. With Django you
define the kind of data your site needs to work with,
and you define the ways your users can work with
that data.


## Creating a project
To start a project we’ll create a new project, create a
database, and start a development server.
Create a new project

```bash
$ django-admin startproject learning_log .
```

Create a database
```bash

$ python manage.py migrate
```

View the project
After issuing this command, you can view the project at
http://localhost:8000/.
$ python manage.py runserver

HOW TO START PROJECT in same dir:

django-admin startproject todo .

## Working with models
The data in a Django project is structured as a set of
models. 
Defining a model
To define the models for your app, modify the file models.py that
was created in your app’s folder. The __str__() method tells
Django how to represent data objects based on this model.

```python
from django.db import models
class Topic(models.Model):
"""A topic the user is learning about."""
text = models.CharField(max_length=200)
date_added = models.DateTimeField(
auto_now_add=True)
def __str__(self):
return self.text
```

Activating a model
To use a model the app must be added to the list
INSTALLED_APPS, which is stored in the project’s settings.py file.

```python
    INSTALLED_APPS = [
      # My apps.
      'learning_logs',
      # Default Django apps.
      'django.contrib.admin',
    ]
```
    
## Building a simple home page

Users interact with a project through web pages, and a
project’s home page can start out as a simple page with no
data. A page usually needs a URL, a view, and a template.

## Mapping a project’s URLs
The project’s main urls.py file tells Django where to find the urls.py
files associated with each app in the project.

    from django.contrib import admin
    from django.urls import path, include
    urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('learning_logs.urls')),
    ]

### Mapping an app’s URLs
An app’s urls.py file tells Django which view to use for each URL in
the app. You’ll need to make this file yourself, and save it in the
app’s folder.

    from django.urls import path
    from . import views
    app_name = 'learning_logs'
    urlpatterns = [
    # Home page.
    path('', views.index, name='index'),
    ]
    
## Writing a simple view
A view takes information from a request and sends data to the
browser, often through a template. View functions are stored in an
app’s views.py file. This simple view function doesn’t pull in any
data, but it uses the template index.html to render the home page.

    from django.shortcuts import render
    def index(request):
    """The home page for Learning Log."""
    return render(request,
    'learning_logs/index.html')

## Writing a simple template
A template sets up the structure for a page. It’s a mix of html and
template code, which is like Python but not as powerful. Make a
folder called templates inside the project folder. Inside the
templates folder make another folder with the same name as the
app. This is where the template files should be saved.
The home page template will be saved as
learning_logs/templates/learning_logs/index.html.

<p>Learning Log</p>
<p>Learning Log helps you keep track of your
learning, for any topic you're learning
about.</p>

## Template inheritance
Many elements of a web page are repeated on every page
in the site, or every page in a section of the site. By writing
one parent template for the site, and one for each section,
you can easily modify the look and feel of your entire site.

## The parent template
The parent template defines the elements common to a set of
pages, and defines blocks that will be filled by individual pages.

    <p>
    <a href="{% url 'learning_logs:index' %}">
    Learning Log
    </a>
    </p>
    {% block content %}{% endblock content %}

## The child template
The child template uses the {% extends %} template tag to pull in
the structure of the parent template. It then defines the content for
any blocks defined in the parent template.

    {% extends 'learning_logs/base.html' %}
    {% block content %}
    <p>
    Learning Log helps you keep track
    of your learning, for any topic you're
    learning about.
    </p>
    {% endblock content %}

## Template indentation
Python code is usually indented by four spaces. In
templates you’ll often see two spaces used for indentation,
because elements tend to be nested more deeply in
templates.

## Another model
A new model can use an existing model. The ForeignKey
attribute establishes a connection between instances of the
two related models. Make sure to migrate the database
after adding a new model to your app.

Defining a model with a foreign key
    
    class Entry(models.Model):
    """Learning log entries for a topic."""
    topic = models.ForeignKey(Topic,
    on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(
    auto_now_add=True)
    def __str__(self):
    return f"{self.text[:50]}..."

## Building a page with data
Most pages in a project need to present data that’s specific
to the current user.

## URL parameters
A URL often needs to accept a parameter telling it which data to
access from the database. The URL pattern shown here looks for
the ID of a specific topic and assigns it to the parameter topic_id.

    urlpatterns = [
    --snip-# Detail page for a single topic.
    path('topics/<int:topic_id>/', views.topic,
    name='topic'),
    ]

## Using data in a view
The view uses a parameter from the URL to pull the correct data
from the database. In this example the view is sending a context
dictionary to the template, containing data that should be displayed
on the page. You'll need to import any model you're using.

    def topic(request, topic_id):
    """Show a topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by(
    '-date_added')
    context = {
    'topic': topic,
    'entries': entries,
    }
    return render(request,
    'learning_logs/topic.html', context)

## Restarting the development server
If you make a change to your project and the change
doesn’t seem to have any effect, try restarting the server:

$ python manage.py runserver

## Using data in a template
The data in the view function’s context dictionary is available
within the template. This data is accessed using template
variables, which are indicated by doubled curly braces.
The vertical line after a template variable indicates a filter. In this
case a filter called date formats date objects, and the filter
linebreaks renders paragraphs properly on a web page.

    {% extends 'learning_logs/base.html' %}
    {% block content %}
    <p>Topic: {{ topic }}</p>
    <p>Entries:</p>
    <ul>
    {% for entry in entries %}
    <li>
    <p>
    {{ entry.date_added|date:'M d, Y H:i' }}
    </p>
    <p>
    {{ entry.text|linebreaks }}
    </p>
    </li>
    {% empty %}
    <li>There are no entries yet.</li>
    {% endfor %}
    </ul>
    {% endblock content %}

## The Django shell
You can explore the data in your project from the command
line. This is helpful for developing queries and testing code
snippets.

Start a shell session
$ python manage.py shell

Access data from the project

    >>> from learning_logs.models import Topic
    >>> Topic.objects.all()
    [<Topic: Chess>, <Topic: Rock Climbing>]
    >>> topic = Topic.objects.get(id=1)
    >>> topic.text
    'Chess'

## Users and forms
Most web applications need to let users create
accounts. This lets users create and work with their
own data. Some of this data may be private, and
some may be public. Django’s forms allow users to
enter and modify their data.

## User accounts
User accounts are handled by a dedicated app called
users. Users need to be able to register, log in, and log
out. Django automates much of this work for you.

## Making a users app
After making the app, be sure to add 'users' to INSTALLED_APPS
in the project’s settings.py file.

$ python manage.py startapp users

## Including URLS for the users app
Add a line to the project’s urls.py file so the users app’s URLs are
included in the project.

    from django.contrib import admin
    from django.urls import path, include
    urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('learning_logs.urls')),
    ]

## Using forms in Django
There are a number of ways to create forms and work with
them. You can use Django’s defaults, or completely
customize your forms. For a simple way to let users enter
data based on your models, use a ModelForm. This creates
a form that allows users to enter data that will populate the
fields on a model.
The register view on the back of this sheet shows a simple
approach to form processing. If the view doesn’t receive
data from a form, it responds with a blank form. If it
receives POST data from a form, it validates the data and
then saves it to the database.


