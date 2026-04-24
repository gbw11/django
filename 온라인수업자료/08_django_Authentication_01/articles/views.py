from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm


def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


def create(request):
    # 사용자가 form을 작성하고 '제출' 버튼을 눌렀을 때 (POST method) - 기존 create 함수
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
        
    # 사용자가 글 생성 링크를 누르거나, URL로 접속한 경우 (GET method) - 기존 new 함수
    else:
        form = ArticleForm()

    # 기존 new, create 함수 공통 코드
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)


def detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    context = {
        'article': article,
    }
    return render(request, 'articles/detail.html', context)


def delete(request, article_id):
    article = Article.objects.get(pk=article_id)
    article.delete()
    return redirect('articles:index')


def update(request, article_id):
    # 1. 수정할 게시글을 DB에서 가져오기 (edit, update 함수 공통)
    article = Article.objects.get(pk=article_id)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(instance=article)

    # edit, update 함수 공통
    context = {
        'form': form,
        'article': article, # 어떤 글을 수정하는지 게시글 pk를 URL로 전달하기 위해 필요
    }
    return render(request, 'articles/update.html', context)