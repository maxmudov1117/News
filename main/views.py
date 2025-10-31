from django.shortcuts import render, get_object_or_404, redirect

from django.views import View
from .models import *


class HomeView(View):
    def get(self, request):
        important_article = Article.objects.filter(important=True, published=True).first()
        articles = Article.objects.filter(important=False, published=True).order_by('-views')[:7]
        lastests = Article.objects.filter(important=False,published=True).order_by('-created_at')[:7]

        q = request.GET.get('q')
        if q:
            articles = Article.objects.filter(title__icontains=q).order_by('-created_at')
            context = {
            'articles': articles,
            }
            return render(request, 'search_results.html', context = context)


        context = {
            'important_article': important_article,
            'articles': articles,
            'lastests':lastests,
        }
        return render(request, 'index.html', context)

    def post(self, request):
        Newsletter.objects.create(email=request.POST.get('email'))

        return redirect('home')

class ArticleDetailsView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        contexts = Context.objects.filter(article=article)
        categories = Category.objects.all()
        articles = Article.objects.all().order_by("-views")[:10]
        tag_ids = article.tag.all().values_list('id', flat=True)
        rel_article = Article.objects.filter(tag__in=tag_ids).exclude(pk=article.pk).distinct()[:2]
        izohlar = Comment.objects.filter(article=article, published=True)[:4]

        context = {
            'article':article,
            'contexts':contexts,
            'categories':categories,
            'articles': articles,
            'rel_article':rel_article,
            'izohlar':izohlar,
        }

        return render(request, 'detail-page.html', context=context)

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        Comment.objects.create(
            article=article,
            author = request.POST.get('name'),
            email = request.POST.get('email'),
            text = request.POST.get('textarea')
        )

        return redirect('article-details', slug=slug)



class CategoryView(View):
    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        articles = category.article_set.filter(published=True).order_by('-created_at')

        context = {
            'articles':articles,
        }

        return render(request, 'category.html', context=context)

class ContactView(View):
    def get(self, request,):
        return render(request, 'contact.html')

    def post(self, request):
        Contact.objects.create(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            subject = request.POST.get('subject'),
            phone = request.POST.get('phone'),
            message = request.POST.get('message')

        )
        return redirect('contact')

