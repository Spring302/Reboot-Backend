# 카카오톡 알림봇 만들기

참고 : https://liwonfather.tistory.com/2

## 단점(개선)

- TOKEN 유지기간이 12시간이라고 쓰여있는데 확인 필요함
  - 실제 6시간이었음. refresh token을 자동으로 받도록 설정함. 다만 2개월 후에 사용자 재인증이 필요하다고 함
- 본인에게 알림은 소리가 안나옴  -> 푸시 알림 기능 사용 시 해결 가능할 지 확인 필요