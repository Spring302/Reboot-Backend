# Re-boot

서버 : django

venv : anaconda base s

> pip install django
> 
> pip install djangorestframework
> 
> pip install markdown       # Markdown support for the browsable API.
> 
> pip install django-filter  # Filtering support


> django-admin startproject config .

> python manage.py runserver

> django-admin startapp <APP NAME>
> rec : 부동산
> bnr : 보안뉴스 추천
> wcf : 워드클라우드 금융
> car : 차 비교


> python manage.py makemigrations [app_name]
> 
> python manage.py migrate [app_name] [migration_name]

## 가상환경
- 가상환경 생성
> python -m venv venv
- 가상환경 활성화
> .\venv\Scripts\activate
- 가상환경 리스트 저장
> pip freeze > requirements.txt
- requirements.txt 설치
> pip install -r requirements.txt
- 가상환경 나가기
> deactivate
