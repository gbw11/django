from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Article
from .serializers import ArticleListSerializer, ArticleSerializer

# Create your views here.
# 4. 모든 DRF의 view함수는 반드시 api_view 데코레이터가 필수
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == "GET":
        # 1. 전체 게시글 조회(DB)
        articles = Article.objects.all()
        # 이 articles는 쿼리셋 형식이여서 다른 서비스들은 이 타입을 활용할 수 없음
        # 직렬화를 진행해서 유연한 데이터 형식으로 변환
        # 2. 직렬화
        # 원물데이터가 단일데이터가 아닌 형식이면 many 옵션을 True로 변경해줘야 한다.
        serializer = ArticleListSerializer(articles, many=True)
        # 3. 직렬화된 데이터 덩어리에서 게시글 데이터만 추출해서 응답
        return Response(serializer.data)

    # 데이터 생성 관련 처리
    elif request.method == "POST":
        # 1. 사용자가 보낸 데이터를 직렬화
        # 과거에는 request.POST에서 추출했지만, DRF에서는 request.data를 사용
        serializer = ArticleSerializer(data=request.data)
        # 2. 유효성 검사(DRF용)
        if serializer.is_valid():
            # 3. 저장
            serializer.save()
            # 4. 저장 후 201 상대 코드를 응답
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # 5. 유효성 검사 실패했다면 400 상태 코드를 응답
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", 'DELETE', 'PUT'])
def article_detail(request, article_id):
    # 1. 단일 게시글 조회
    article = Article.objects.get(pk=article_id)    
    if request.method == 'GET':
        # 2. 직렬화
        serializer = ArticleSerializer(article)
        # 3. 직렬화된 데이터에서 필요한 데이터만 추출하여 응답
        return Response(serializer.data)
    
    elif request.method == "DELETE":
        # 조회된 게시글 데이터를 삭제
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PUT":
        # 1. 사용자가 보낸 수정 데이터를 직렬화
        # 그런데 수정이기 때문에 기존 객체를 함게 넣어서 직렬화를 진행
        serializer = ArticleSerializer(article, data=request.data)
        # serializer = ArticleSerializer(instance=article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # 2. 저장 후 201 상대 코드를 응답
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # 3. 유효성 검사 실패했다면 400 상태 코드를 응답
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
