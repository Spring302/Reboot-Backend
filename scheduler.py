import schedule
import time
import datetime
import sys

# 스케쥴 모듈이 동작시킬 코드 : 현재 시간 출력
def test_function():
    now = datetime.datetime.now()
    print(f"Date: [{now}]")


# 프로그램을 종료시키기 위한 함수
def exit():
    print("scheduler exit")
    sys.exit()


# 1초마다 test_fuction을 동작시키다가 "22:21"이 되면 프로그램 종료
schedule.every(1).seconds.do(test_function)
schedule.every().day.at("22:21").do(exit)


# 무한 루프를 돌면서 스케쥴을 유지한다.
while True:
    schedule.run_pending()
    time.sleep(1)
