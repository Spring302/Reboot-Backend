# REBOOT - Side Project

- 실용적인 개발을 추구하며 실제로 필요한 기능들을 직접 만들어 나가는 프로젝트입니다.

## 🎢부동산 최저가 알림봇 만들기(REC: Real Estate Crawling)

- 원하는 아파트의 최저가를 매일 크롤링합니다.
- 아파트 실거래가가 아닌 매물의 매매/전세 최저가를 알 수 있어 실제 내집마련에 도움이 될 수 있도록 구현했습니다.
- 매물가격의 추이를 기록하기 때문에 실거래가 없더라도 가격이 떨어지고 있는지, 올라가는지 파악할 수 있습니다.
- 모두 내집마련하시기 바랍니다.
- 다음 프로젝트 목표는 주식!

## 실행방법

- docker-compose up -d

## 시스템 구성

- Backend : Django (Django Rest Framework)
- DB : PostgreSQL
- Infra : Docker
- Frontend : Vue.js

## 사용된 모든 Skills

- Django, Django ORM, DjangoRestFramework, SQL, PostgreSQL, Django Cron, Scheduler
- Vue.js, Html, Css, Javascript, node.js, Bootstrap
- Swagger, Selenium, Beautifulsoup, DotENV, Slack API, Kakao API, CORS
- Docker, Docker-Compose

## 데이터베이스 설계

[MyApart](https://www.erdcloud.com/d/XpfmrNRfoRWaub9jy)

## API 설계

- 기타 API는 Swagger을 참고해주세요.

| INDEX | METHOD | URL | DESCRIPTION |
| --- | --- | --- | --- |
| 1 | GET | /apart | 조회할 아파트 리스트 조회 |
| 2 | POST | /apart | 조회할 아파트 추가 |
| 3 | GET | /apart/{id} | ID별 아파트 조회 |
| 4 | PUT | /apart/{id} | ID별 아파트 수정 |
| 5 | DELETE | /apart/{id} | ID별 아파트 삭제 |
| 6 | GET | /apart/price | 전체 아파트 가격 조회 |
| 7 | POST | /apart/price | 아파트 가격 추가 |
| 8 | GET | /apart/price/{id} | ID별 아파트 가격 조회 |
| 9 | PUT | /apart/price/{id} | ID별 아파트 가격 수정 |
| 10 | DELETE | /apart/price/{id} | ID별 아파트 가격 삭제 |
| 11 | GET | /apart/today | 오늘의 가격 조회 |

## 고민의 흔적들🤣

[(진행과정)부동산 최저가 알림봇 만들기](https://www.notion.so/8141d6624c574eef93641b1609746568)