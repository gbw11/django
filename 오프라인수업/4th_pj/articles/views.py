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

# 페이지 렌더링(단순 조회 목적(get요청))
def new(request):
    return render(request, 'articles/new.html')


# 페이지 리다이렉트(데이터 저장 or 변경(post요청))
def create(request):
    # 첫번째 방법
        # 조회 => 변수 할당 => save()
        # article = Article()
        # article.title = 'first'
        # article.content = 'hello'
        # article.save()

    # 두번째 방법
        # article = Article(title = 'third', content = 'byebye')
        # article.save()
    
    # 세번째 방법
        # Article.objects.create(title = 'third', content = 'byebye')
    
    ## 두번째 방법을 지향하고, 세번째는 지양
        # why? : 데이터를 DB에 저장할 떄는 반드시 데이터를 검증하고 save() 해야한다.
        # 검증단계 => 유효성 검사.. 등등 : 세번째는 검증이 불가능!
    title = request.POST.get('title') # .get('title')  => form태그에서 name으로 넘겨준것
    content = request.POST.get('content')
    # 2번 방법 : 코드가 간결하면서도 안정성
    article = Article(title = 'title', content = content)
    article.save()

    return redirect('articles:detail', article.pk)

# 페이지 렌더링
# create와 차이 : 기존에 있던 게시글 조회
def edit(request, pk):
    # queryset API 방법
    article = Article.objects.get(pk = pk)
    context = {
        'article' : article
    }

    return render(request, 'articles/edit.html', context)

# create와 차이 : 기존에 있던 게시글을 변경(DB 레코드 변경)
def update(request, pk):
    # queryset API 방법, 먼저 조회하고
    article = Article.objects.get(pk = pk)
    # 기존의 article을 변경
    article.title = request.HOST.get('title')
    article.content = request.HOST.get('content')
    article.save()
    
    return redirect('articles : detail', article.pk)

# 단일 게시글 조회 후 삭제
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    # POST 요청 => DB변경 : redirect

    return redirect('articles:index')