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

create database rec;

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

python manage.py makemigrations
python manage.py migrate

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
    serializer_class  = ApartmentsSerializer

class ApartmentstDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Apartments.objects.all()
    serializer_class  = ApartmentsSerializer
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
- 다만 아직 버그가 있어서 runserver 시 2번 로딩을 하고 스케쥴러도 두번 작동은 한다.
  - 해결방법은 `python manage.py runserver --noreload` 로 시작하면 된다.
  
