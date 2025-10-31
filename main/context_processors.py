from django.shortcuts import render, get_object_or_404, redirect

from main.models import *

from django.views import View


def categories(request):
    categories = Category.objects.all()

    return {'categories':categories}

def articles(request):
    articles = Article.objects.filter(important=False,published=True).order_by('-views')[:1]
    context = {
        'articles':articles,
    }
    return context