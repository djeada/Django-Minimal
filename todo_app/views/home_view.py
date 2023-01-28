from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    """
    Render the home page.

    :param request: the request object
    :return: the rendered home page
    """
    return render(request, "../templates/home.html")
