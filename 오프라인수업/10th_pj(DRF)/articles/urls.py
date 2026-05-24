from django.urls import path
from articles import views

# app_name = 'articles' 안쓴다.
# template가 없기 때문에

urlpatterns = [
    # 전체 게시글 조회, 게시글 생성
    path('articles/', views.article_list),
]