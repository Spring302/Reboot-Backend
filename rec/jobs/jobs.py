from datetime import datetime
import psycopg2
from rec.utils.cron import Cron

from rec.utils.slackbot import SlackAPI
from slack_sdk.errors import SlackApiError
import os

SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
CHANNEL_NAME = "test"
TEXT = "자동 생성 문구 테스트"


def schedule_api():
    # TODO: insert data to DB
    print("schedule_api : successful")
    with psycopg2.connect(database='reboot', user='reboot', password='reboot') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM rec_apartments")
        apartments = cur.fetchall()
        info_list = Cron.crawling_rec_tuple(apartments)  # list of dict_data
        for info in info_list:
            cur.execute("""
            INSERT INTO rec_priceinfo (apart_id, date, price, per_price)
            VALUES (%s, %s, %s, %s)
            """, (info['apart'], info['date'], info['price'], info['per_price']))
            con.commit()


def schedule_api2():
    with psycopg2.connect(database='reboot', user='reboot', password='reboot') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM rec_priceinfo")
        apartments = cur.fetchall()
        print(apartments)

    # try:
    #     slack = SlackAPI(SLACK_TOKEN)

    #     # 채널ID 파싱
    #     channel_id = slack.get_channel_id(CHANNEL_NAME)

    #     slack.client.chat_postMessage(
    #         channel=channel_id,
    #         text=TEXT,
    #     )

    # except SlackApiError as e:
    #     # You will get a SlackApiError if "ok" is False
    #     assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'
