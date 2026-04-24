from django import forms
from .models import Article

# form 태그 사용해서 name으로 넘겨주고 DB에 저장 가능
# 단, 로직을 수동으로 구현해줘야함
# ModelForm은 form.save()하면 바로 DB에 저장
# 왜 쓸까? 편의성 + 유효성검사에 용이하다.

class ArticleForm(forms.ModelForm):
    # class Meta -> 모델폼의 기본구조를 자동으로 생성
    # 단점 : css 거의 불가능
    # 장점 : 위젯으로 세부 조정 가능
    class Meta:
        model = Article
        # fields = ('title', 'content', 'created_at', 'updated_at', )
        fields = '__all__'