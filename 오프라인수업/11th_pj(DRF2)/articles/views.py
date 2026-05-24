from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Article, Comment
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer

# list : 전체 객체 조회, object : 단일 객체 조회
# 4xx : 클라이언트 에러
# 5xx : 서버 에러
# 404 : not found
from django.shortcuts import get_list_or_404, get_object_or_404

# GET : 조회
# POST : 생성
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
        
       
@api_view(["GET", "PUT", "DELETE"])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    # 단일 게시글 조회
    if request.method == "GET":
        # 직렬화 => 응답
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    # 게시글 삭제
    elif request.method ==  "DELETE":
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == "PUT":
        # request.data : title, content
        # partial=True : 부분 업데이트 허용(일부 필드만 수정 가능)
        serializer = ArticleSerializer(
            article, data=request.data, partial=True
        )
        # raise_exception : 유효하지 않을 경우 예외 발생
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # return Response(serializer.error, status = status.HTTP_400_BAD_REQUEST) => raise_exception 때문에 이렇게 작성하지 않아도 된다.
            return Response(serializer.data)
        
@api_view(["GET"])
def comment_list(request):
    # 댓글 하나도 없으면 404 에러
    comments = get_list_or_404(Comment)
    # 직렬화
    serializer = CommentSerializer(comments, many=True)
    
    return Response(serializer.data)

@api_view(["GET", "DELETE", "PUT"])
def comment_detail(request, comment_pk):
    # 댓글부터 조회
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == "GET":
        # 직렬화 => json으로 응답
        seriazlizer = CommentSerializer(comment)
        return Response(seriazlizer.data)

    elif request.method == "DELETE":
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        seriazlizer = CommentSerializer(
            comment, data=request.data, partial=True
        )
        # raise_exception : 400_BAD_REQUEST 에러 발생시켜줌
        if seriazlizer.is_valid(raise_exception=True):
            seriazlizer.save()
            return Response(seriazlizer.data)
        
@api_view(['POST'])
def comment_create(request, article_pk):
    # 게시글부터 조회
    article = get_object_or_404(Article, pk=article_pk)
    # request.data : content
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(article=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)