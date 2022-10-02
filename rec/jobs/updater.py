from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import *


def start():
    scheduler = BackgroundScheduler(timezone='Asia/Seoul')
    # scheduler.add_job(schedule_api, 'cron', hour=9, minute=0, second=0)
    # scheduler.add_job(schedule_message_api, 'cron', hour=9, minute=0, second=0)
    schedule_api2()
    scheduler.start()
