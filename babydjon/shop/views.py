from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from shop.models import Category
import shop.contexts as contexts

indexContext = contexts.indexContext()

def index(request):
    return render(request, "shop/index.html", indexContext)

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")