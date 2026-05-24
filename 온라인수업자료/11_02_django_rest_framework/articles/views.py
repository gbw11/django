from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from .models import Article, Comment
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer

# Create your views here.
# 4. 모든 DRF의 뷰함수는 반드시 api_view 데코레이터가 필수
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        # 1. 전체 게시글 조회 (DB)
        articles = Article.objects.all()
        # 그런데 articles는 쿼리셋 형식이어서 다른 서비스들은 이 타입을 활용할 수가 없음
        # 직렬화를 진행해서 유연한 데이터 형식으로 변환
        # 2. 직렬화
        # 원물 데이터가 단일 데이터가 아닌 형식이면 many 옵션을 True로 변경해줘야 함
        serializer = ArticleListSerializer(articles, many=True)
        # 3. 직렬화된 데이터 덩어리에서 게시글 데이터만 추출해서 응답
        return Response(serializer.data)

    # 데이터 생성 관련 처리
    elif request.method == 'POST':
        # 1. 사용자가 보낸 데이터를 직렬화
        # 과거에는 request.POST에서 추출했지만, DRF에서는 request.data를 사용
        serializer = ArticleSerializer(data=request.data)
        # 2. 유효성 검사
        if serializer.is_valid():
            # 3. 저장
            serializer.save()
            # 4. 저장 후 201 상태 코드를 응답
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 5. 유효성 검사 실패했다면 400 상태 코드를 응답
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


from django.db.models import Count

@api_view(['GET', 'DELETE', 'PATCH'])
def article_detail(request, article_id):
    # 1. 단일 게시글 조회
    # article = Article.objects.get(pk=article_id)
    
    # 1-1. 게시글 가져오면서 + 해당 게시글의 댓글의 갯수까지 계산해서 조회
    article = Article.objects.annotate(num_of_comments = Count('comments_list')).get(pk=article_id)
    

    if request.method == 'GET':
        # 2. 직렬화
        serializer = ArticleSerializer(article)
        # 3. 직렬화된 데이터에서 필요한 데이터만 추출하여 응답
        return Response(serializer.data)

    elif request.method == 'DELETE':
        # 조회된 게시글 데이터를 삭제
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        # 1. 사용자가 보낸 수정 데이터를 직렬화
        # 그런데 수정이기 때문에 기존 객체를 함께 넣어서 직렬화를 진행
        serializer = ArticleSerializer(
            article, data=request.data, partial=True
        )
        # serializer = ArticleSerializer(instance=article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # 2. 갱신 후 200 상태 코드를 응답
            return Response(serializer.data)
        # 3. 유효성 검사 실패했다면 400 상태 코드를 응답
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def comment_list(request):
    # 1. 댓글 목록 조회
    comments = Comment.objects.all()
    # 2. 댓글 목록 쿼리셋을 직렬화
    serializer = CommentSerializer(comments, many = True)
    # 3. 댓글 데이터를 추출하여 응답
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, comment_id):
    # 1. 단일 댓글 조회
    comment = Comment.objects.get(pk=comment_id)
    if request.method == "GET":
        # 2. 직렬화
        serializer = CommentSerializer(comment)
        # 3. 댓글 데이터를 추출하여 응답
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # 1. 사용자가 입력한 댓글 데이터를 직렬화
        # comment : 기존 댓글  => 댓글 갱신함을 알리기 위함
        serializer = CommentSerializer(comment, data=request.data)
        # 2. 유효성 검사
        if serializer.is_valid(raise_exception=True):
            # 게시글 조회(article=article) 을 넣어줄 필요가 없음
            # => serializer 호출할 때 첫번재 인자로 comment(외래키) 불러왔기 때문
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def comment_create(request, article_id):
    # 1. 게시글을 먼저 조회
    article = Article.objects.get(pk=article_id)
    # 2. 사용자가 댓글 데이터를 조회
    serializer = CommentSerializer(data=request.data)
    # 3. 유효성 검사
    # raise_exception : 400번대 에러 코드 자동으로 보내줌
    if serializer.is_valid(raise_exception=True):
        # 5. 누락된 외래 키 데이터를 추가해서 저장
        serializer.save(article=article)
        # 4. 저장 후 201 상태 코드를 응답
        return Response(serializer.data, status=status.HTTP_201_CREATED)
