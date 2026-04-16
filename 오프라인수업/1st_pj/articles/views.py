from django.shortcuts import render

# Create your views here.

def index(request):
    # page를 렌더링 하겠다.
    # 렌더링 : html페이지를 하나 띄운다.
    # 두번쩨 인자 : 경로 (자동으로 templates에 접근)
    return render(request, 'articles/index.html')