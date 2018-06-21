from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from django.http import Http404

# Create your views here.
def page_view(request, page_name):
    # 1. Попытаться вывести шаблон page_name.html
    # 2. Если его нет, сообщить, что страницы нет