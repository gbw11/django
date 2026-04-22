* Django Shell 환경에서 연습할 코드입니다.
* 복사 / 붙여넣기를 통해서 활용해주세요.
* ipython 라이브러리 설치가 필요합니다. 
  * `pip install ipython`
  * `pip freeze > requirements.txt`

* 실습 전에 Django Shell 환경 실행이 필요합니다.
  * 실행 명령어:  `python manage.py shell -v 2` 

-------
# QuerySet API 실습
> 실습은 한 줄 씩 복사해서 붙여넣어주세요.

## Create 실습

### 첫 번째 방식
* 빈 객체 생성 후 값 할당 후 저장
```python
# 빈 객체 생성
article1 = Article()

# title 정보 작성
article1.title = 'first'

# content 정보 작성 
article1.content = 'django!'

# 데이터베이스에 저장
article1.save()

# 데이터베이스 Article 테이블에 저장된 모든 데이터 읽어서 확인
Article.objects.all()

```

### 두 번째 방식
```python
# 객체를 생성할 때 초기 값을 넣어서 생성
article2 = Article(title='second', content='django!')

# 데이터베이스에 저장
article2.save()

# 데이터베이스 Article 테이블에 저장된 모든 데이터 읽어서 확인
Article.objects.all()

```

### 세 번째 방식
```python
# QuerySet API 인 create를 통해 한 번에 생성 및 저장
Article.objects.create(title='third', content='django!')

# 데이터베이스 Article 테이블에 저장된 모든 데이터 읽어서 확인
Article.objects.all()
```

-------
## Read 실습
### all() 실습
* 모든 데이터를 조회
* 데이터가 0개 이상이 존재할 수 있음
  * QuerySet으로 결과를 반환
```python
 Article.objects.all()
```

### filter() 실습
* 주어진 매개변수와 일치하는 데이터를 반환
* 일치하는 데이터가 0개 이상일 수 있음
  * QuerySet으로 결과를 반환
```python
# content가 django!인 데이터 조회
Article.objects.filter(content='django!')

# title이 abc인 데이터 조회
Article.objects.filter(title='abc')

# title이 first인 데이터 조회
Article.objects.filter(title='first')
```
### get() 실습
* 오직 1개의 데이터를 가져올 때 사용
  * 일치하는 객체 1개만 반환
* 여러 개 있거나 없으면 에러 발생
```python
# 일치하는 데이터가 존재하는 경우
Article.objects.get(pk=1)
# 결과: <Article: Article object (1)>

# 일치하는 데이터가 없는 경우
Article.objects.get(pk=100)
# 결과: DoesNotExist: Article matching query does not exist.

# 일치하는 데이터가 여러 개 인 경우
Article.objects.get(content='django!')
# 결과: MultipleObjectsReturned: get() returned more than one Article -- it returned 2!
```

-------

## Update 실습
1. DB에서 수정할 데이터를 가져온다.
2. 데이터를 수정한다.
3. 저장한다.

```python
# 1. 수정할 데이터를 가져온다.
article = Article.objects.get(pk=1)

# 2. 데이터를 수정한다.
article.title = 'byebye'

# 3. 저장한다.
article.save()
```

-------

## Delete 실습
1. 삭제할 데이터를 가져온다.
2. 삭제한다.

```python
# 1. 삭제할 데이터를 가져온다.
article = Article.objects.get(pk=1)

# 2. 삭제한다.
article.delete()
```