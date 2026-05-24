from rest_framework import serializers
from .models import Article, Comment


# 단일 게시글 데이터(단일 인스턴스)를 직렬화 하는 도구
# 그러면 ArticleListSerializer를 단일 게시글에서는 못쓰나요? ==> NO
class ArticleSerializer(serializers.ModelSerializer):
    
    # 단일 게시글 + 댓글 목록 조회를 위해 댓글 목록 직렬화 도구를 작성
    class CommentDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ('id', 'content',)
    
    # 기존에 article이 가지고 있는 역참조 매니저인 commnet_set의 값을
    # CommentDetailSerializer 댓글 결과 목록으로 재정의
    comments_list = CommentDetailSerializer(read_only=True, many=True)
    
    # 완전히 새로운 필드를 선언(댓글 개수)
    num_of_comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = '__all__'
    
    # 위에서 추가하는 num_of_commnets 필드의 값을 반환하는 메서드 정의
    def get_num_of_comments(self, obj):
        # obj : Serializer 클래스가 처리하는 모델(Article) 클래스의 인스턴스
        # 그래서 해당 게시글 객체를 활용하여 코드를 작성 가능
        return obj.num_of_comments
    
        # 만약에 view에서 annotate를 사용하지 않았다면,
        # num_of_comments = obj.comment_set.count()
        # return self.num_of_comments

# 전체 게시글 데이터(쿼리셋)를 직렬화 하는 도구
class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content',)

class CommentSerializer(serializers.ModelSerializer):

    # [댓글 제이터 제공할 때 댓글이 작성된 게시글의 번호와 제목도 함께 제공하기 위한 추가 데이터 설정]
    # 게시글의 제목을 직렬화 할 수 있는 도구를 생성
    class ArticleTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ('id', 'title',)

    # 기존 읽기 전용 필드인 article 필드를 위해 도구(ArticleTitleSerializer)의 결과값으로 재정의
    # 기존 필드를 재정의 할때는 Meta 클래스에서 작성했던 read only fields가 먹히지 않게 됨
    # 다른 방법으로 읽기 전용 필드를 설정 => read_only=True
    article = ArticleTitleSerializer(read_only=True)


    class Meta:
        model = Comment
        fields = '__all__'
        # read_only_fields = ('article',)