from rest_framework import serializers

from .models import Article, Comment

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        # 직렬화 하고자 하는 필드
        fields = (
            'id',
            'title',
            'content',
        )

class ArticleSerializer(serializers.ModelSerializer):
    # 게시글 안에 있는 댓글 => 중첩
    class CommentDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = (
                'id',
                'content'
            )
    # read_only : 읽기 전용
    # 1. 사용자로 입력받지 않는다.
    # 2. 유효성 검사 과정에서 제외
    # 3. 입력받는 데이터는 없지만 응답 결과는 클라이언트에 제공
    comment_set = CommentDetailSerializer(many=True, read_only=True)
    
    comment_count = serializers.IntegerField(
        source = 'comment_set.count', read_only=True
    )

    class Meta:
        model = Article
        # 직렬화 하고자 하는 필드
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    # 댓글 조회했을 때 게시글의 제목(title)이 같이 나오게
    class ArticleTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ('title',)
    # 댓글 조회했을 때 같이 조회되는 게시글의 제목도 읽기 전용
    article = ArticleTitleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'