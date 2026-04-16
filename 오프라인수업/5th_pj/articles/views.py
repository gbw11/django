from django.shortcuts import render, redirect

# Create your views here.
from .models import Article

def index(request):
    # QuerySet AIP -> 전체 데이터 조회 : Article.objects.all()
    articles = Article.objects.all()

    context ={
        'articles' : articles
    }

    return render(request, 'articles/index.html', context)


def detail(request, pk):
    # QuerySet API => 단일 데이터 조회 : get
    article = Article.objects.get(pk = pk)
    context = {
        # 단일 데이터여서 s안붙임
        'article' : article
    }

    # articles 폴더에 있는 detail.html 파일을 랜더링하겠다. context를 넘겨주면서

    return render(request, 'articles/detail.html', context)

from .forms import ArticleForm

# 페이지 렌더링 + 리다이렉트
def create(request):
    # submit버튼 눌렀을 때!
    if request.method == "POST":
        form = ArticleForm(request.POST)
        # 1. 모든 필수 필드가 채워져있는지
        # 2. 입력된 데이터가 필드 조건을 만족하는지(데이터 타입, 길이 제한)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
        
    else: # submit버튼 누르기 전, 다른 버튼(다른 요청 일떄)
        form = ArticleForm() # 빈폼

    # GET요청
    context = {
        'form' : form
    }
    return render(request, 'articles/create.html', context)

# 페이지 렌더링
# create와 차이 : 기존에 있던 게시글 조회
def update(request, pk):
    # 조회 먼저하고
    article = Article.objects.get(pk=pk)
    # submit버튼 눌렀을 때
    if request.method == "POST":
        # 기존 게시글의 데이터를 미리 채운다(instance = article)
        form = ArticleForm(request.POST, instance = article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article.pk)
        
    else: # POST 요청이 아닐 때
        form = ArticleForm(instance = article)
    context = {
        'article' : article,
        'form' : form
    }
    return render(request, 'articles/update.html', context)

# 단일 게시글 조회 후 삭제
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    # POST 요청 => DB변경 : redirect

    return redirect('articles:index')