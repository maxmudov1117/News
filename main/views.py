from django.shortcuts import render, get_object_or_404, redirect

from django.views import View
from .models import *


class HomeView(View):
    def get(self, request):
        important_article = Article.objects.filter(important=True, published=True).first()
        articles = Article.objects.filter(important=False, published=True).order_by('-views')[:7]
        lastests = Article.objects.filter(important=False,published=True).order_by('-created_at')[:7]

        context = {
            'important_article': important_article,
            'articles': articles,
            'lastests':lastests,
        }
        return render(request, 'index.html', context)

    def post(self, request):
        Newsletter.objects.create(email=request.POST['email'])

        return redirect('home')

