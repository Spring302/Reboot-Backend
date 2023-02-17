from datetime import datetime
import psycopg2
from rec.utils.cron import Cron
from django.db import connection

from utils.slackbot import SlackAPI
from utils.kakaobot import Kakaobot
import os
from pathlib import Path
import environ

env = environ.Env(DEBUG=(bool, False))

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(env_file=os.path.join(BASE_DIR, "env/.env"))

database = env("DB_NAME")
user = env("DB_USER")
password = env("DB_PASS")


def schedule_api():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM rec_apartments")
        apartments = cursor.fetchall()
        info_list = Cron.crawling_rec_tuple(apartments)  # list of dict_data
        for info in info_list:
            print(info)
            cursor.execute(
                """
            INSERT INTO rec_priceinfo (apart_id, date, price, per_price)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (apart_id, date) DO UPDATE 
            SET price = %s, per_price = %s
            """,
                (
                    info["apart"],
                    info["date"],
                    info["price"],
                    info["per_price"],
                    info["price"],
                    info["per_price"],
                ),
            )
            print("1")
            connection.commit()
            print("schedule_api 완료")


def schedule_api2():
    with connection.cursor() as cursor:
        cursor.execute(
            """
        SELECT b.name, a.transaction_style, a.price, a.per_price, a.date
        FROM rec_priceinfo a
        INNER JOIN rec_apartments b 
        ON b.id = a.apart_id
        WHERE a.date = CURRENT_DATE
        ORDER BY a.apart_id ASC"""
        )
        apartments = cursor.fetchall()
        apart_list = print_apart_list(apartments)
        print(apart_list)
        # kakaobot = Kakaobot()
        # kakaobot.send_message(apart_list)
        # slack = SlackAPI()
        # slack.send_message(apart_list)


def print_apart_list(apartments):
    text = ""

    for apartment in apartments:
        name = apartment[0]
        transaction_style = apartment[1]
        price = apartment[2]
        per_price = apartment[3]
        # date = apartment[4]
        text += f"{name}({transaction_style}):{price}만원(평당{per_price}만원)\n"

    return text
