from django.urls import path
from articles import views

# app_name = 'articles' 안쓴다.
# template가 없기 때문에

urlpatterns = [
    # 전체 게시글 조회, 게시글 생성
    path('articles/', views.article_list),
    # 단일 게시글 조회, 삭제, 수정
    path('articles/<int:article_pk>/', views.article_detail),
    # 전체 댓글 조회
    path('comments/', views.comment_list),
    # 단일 댓글 조회, 삭제, 수정
    path('comments/<int:comment_pk>/', views.comment_detail),
    # 게시글로부터 댓글 생성
    path('articles/<int:article_pk>/comments/', views.comment_create),
]