# 부동산 가격 알림봇

## venv

```bash
# from git bash
source ./back/venv/Scripts/activate
```

## 확인 방법

`python manage.py shell`

```bash
from rec.models import *        
from rec.serializers import *       
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

apart = Apartments(name="부영 1차")
apart.save()

serializer = ApartmentsSerializer(apart)   
serializer.data
# {'id': 2, 'name': '부영 1차'}

# 파이썬 네이티브 데이터 모델로 변환(serialization)
content = JSONRenderer().render(serializer.data) 
content
# b'{"id":2,"name":"\xeb\xb6\x80\xec\x98\x81 1\xec\xb0\xa8"}'

# Deserialization 
import io
stream = io.BytesIO(content)
data = JSONParser().parse(stream)
data
# {'id': 2, 'name': '부영 1차'}

serializer = ApartmentsSerializer(data=data)
serializer.is_valid()
serializer.validated_data
serializer.save()

# 저장된 전체 데이터 확인
serializer = ApartmentsSerializer(Apartments.objects.all(), many=True)
serializer.data
```

## DB 생성

`create database rec;`

## postgresql 계정 생성 및 권한 설정

```SQL
create user reboot with password 'reboot';
alter role reboot set client_encoding to 'utf-8';
alter role reboot set timezone to 'Asia/Seoul';
drop database reboot;
create database reboot;
grant all privileges on database reboot to reboot;
```

## migrate

```bash
python manage.py makemigrations
python manage.py migrate
```

성공 시 아래와 같이 뜬다.

```bash
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, rec, sessions, snippets
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying snippets.0003_alter_snippet_language_alter_snippet_style... OK
(venv) 
```

잘 안될 경우 `drop databese reboot` 로 db 삭제 후 다시 만들어서 시도해보자.

```bash
# POST using JSON
http --json POST http://127.0.0.1:8000/apart/ name="빛가람코오롱"
## https://www.django-rest-framework.org/tutorial/2-requests-and-responses/
```

## Views

django-rest-framework 의 가장 최적화된 코드는 다음과 같다.

```python
# views.py
from rest_framework import generics

from rec.models import *
from rec.serializers import *

# (중요) queryset, serializer_class 로 변수명을 고정시켜야 한다. 내부적으로 저 변수명을 호출하는 듯 하다
class ApartmentsList(generics.ListCreateAPIView):
    queryset = Apartments.objects.all()
    serializer_class = ApartmentsSerializer

class ApartmentstDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Apartments.objects.all()
    serializer_class = ApartmentsSerializer
```

## scheduler 만들기

> django에서는 사용이 어렵다. 아래 APScheduler 이용하자.

```python
pip install schedule

# scheduler.py

import schedule
import time

def job():
    print("I'm working...")

schedule.every(10).seconds.do(job)
schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every(5).to(10).minutes.do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)
schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
```

## 매매가 저장

```python
from rec.models import *
from rec.serializers import *

# params
apart_id = 1
price = 1300

# 매매가 저장
apart = Apartments.objects.get(id=apart_id)
price = PriceInfo(apart=apart, price=price)
price.save()

# 데이터 확인
serializer = PriceInfoSerializer(price)
serializer.data
```

## 특정 날자의 데이터 가져오기

```python
# 하나만 가져오기
Entity.objects.get(id=1)
# 여러개 가져오기
Entity.objects.filter(date='2022-01-15')

class TodayApartmentsList(generics.ListAPIView):
    today = datetime.today().strftime('%Y-%m-%d')
    queryset = PriceInfo.objects.filter(date=today)
    serializer_class = PriceInfoSerializer
```

## APScheduler 이용 스케쥴러 만들기

> 참고 : https://ffoorreeuunn.tistory.com/466

- 윈도우에서 스케쥴러 사용을 위해 APScheduler를 사용한다.
- 다만 runserver 시 서버가 두 번 실행되는 문제가 있다.
  - 해결방법은 `python manage.py runserver --noreload` 로 시작하면 된다.
  - 문제원인 : http://blog.quantylab.com/django_onstartup.html
  
## DotENV 폴더 생성
- Github에 올릴 시 개인정보(비밀번호)가 노출되었다는 알림이 자주 와서 공부하게 되었다.
- .env 파일을 만들고, pip install django-environ 을 설치하여 개인정보 노출을 방지할 수 있다.
- 예제 : https://pypi.org/project/django-environ/ 

## Django ORM Cookbook

https://django-orm-cookbook-ko.readthedocs.io/en/latest/query.html

## Executing custom sql directly

https://docs.djangoproject.com/en/4.1/topics/db/sql/#executing-custom-sql-directly

## Windows/Linux Scheduler 구현

- windows에서 django scheduler 구현방법에 대해 다시 알아보았다.
- 이 경우에는 스케쥴러 따로, 백엔드 따로 동작이 필요한것같다.

  ```python
  # pip install schedule
  import schedule
  import time
  import datetime
  import sys

  #스케쥴 모듈이 동작시킬 코드 : 현재 시간 출력
  def test_function():
      now = datetime.datetime.now()
      print(f"Date: [{now}]")

  #프로그램을 종료시키기 위한 함수
  def exit():
      print("scheduler exit")
      sys.exit()
      
  #1초마다 test_fuction을 동작시키다가 "22:21"이 되면 프로그램 종료
  schedule.every(1).seconds.do(test_function)
  schedule.every().day.at("22:21").do(exit)


  #무한 루프를 돌면서 스케쥴을 유지한다.
  while True:
      schedule.run_pending()
      time.sleep(1)
  # python scheduler.py
  ```

- 참고 : https://ybworld.tistory.com/74

## Django Swagger

- https://django-rest-swagger.readthedocs.io/en/latest/#quick-start