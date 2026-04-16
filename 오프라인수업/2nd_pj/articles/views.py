from django.shortcuts import render

# Create your views here.
def index(request):
    # context는 딕셔너리 구조
    # templates에서 context의 key값으로 접근
    context = {
        'name' : "Bokyeom",
        'number' : 1,
    }
    # render의 3번째 인자는 context
    # templates의 articles의 index.html을 랜더링하고 context를 넘겨주겠다.
    return render(request, 'articles/index.html', context)

import random
def dinner(request):
    foods = ["족발", "보쌈", "치킨", "피자"]
    picked = random.choice(foods)
    context = {
        'foods' : foods,
        'picked' : picked,
    }

    return render(request, 'articles/dinner.html', context)

def search(request):

    return render(request, 'articles/search.html')

def throw(request):
    # throw페이지에서는 form태그로 던진다.
    return render(request, 'articles/throw.html')

def catch(request):
    # form태그의 name이 뭘까가 중요
    # name ="throw"
    # GET : GET방식, .get : 딕셔너리 메서드
    # text = request.GET.get('throw')   => GET['throw'] 상관없음
    text = request.GET.get('throw')
    context = {
        'text' : text
    }
    return render(request, 'articles/catch.html', context)

def detail(request, number):

    context = {
        'number' : number
    }
    return render(request, 'articles/detail.html', context)