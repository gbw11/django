from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Article
from .serializers import ArticleListSerializer, ArticleSerializer

# list : 전체 객체 조회, object : 단일 객체 조회
# 4xx : 클라이언트 에러
# 5xx : 서버 에러
# 404 : not found
from django.shortcuts import get_list_or_404, get_object_or_404

# get : 조회
# post : 생성

@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == "GET":
        # 하나의 게시글이라도 조회가 안되면 404 error
        articles = get_list_or_404(Article)
        # 다중 데이터(여러개의 객체)일 때 : many = True
        serializer = ArticleListSerializer(articles, many=True)
        # 직렬화된 데이터를 json 형식으로 response
        return Response(serializer.data)
    
    elif request.method == "POST":
        # articles = get_object_or_404
        serializer = ArticleSerializer(data=request.data)
        # raise_exception=True : 유효하지 않을 경우 예외 발생
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # 데이터 생성에 성공 : HTTP_201, 실패 : HTTP_400
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
