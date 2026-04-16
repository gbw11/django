from django.db import models

# Create your models here.

class Article(models.Model):

    # Q) 왜 title은 글자제한이 있고, content는 없을까?
    #     A) title(게시글 제목)에 글자제한이 없다면 악용 가능(광고, 암표, 도배 등..)
    title = models.CharField(max_length=20)
    content = models.TextField()
    # auto_now_add : 객체가 처음 생성될 때 시간 
    created_at = models.DateTimeField(auto_now_add = True)
    # auto_now : 객체가 저장(수정)될 때마다 시간
    updated_at = models.DateTimeField(auto_now = True)