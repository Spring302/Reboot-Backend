from datetime import datetime
import psycopg2
from rec.utils.cron import Cron

from utils.slackbot import SlackAPI
from utils.kakaobot import Kakaobot


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
        cur.execute("""
        SELECT b.name, a.price, a.per_price, a.date
        FROM rec_priceinfo a
        INNER JOIN rec_apartments b 
        ON b.id = a.apart_id
        WHERE a.date = CURRENT_DATE
        ORDER BY a.apart_id ASC""")
        apartments = cur.fetchall()
        apart_list = print_apart_list(apartments)
        kakaobot = Kakaobot()
        kakaobot.send_message(apart_list)
        # slack = SlackAPI()
        # slack.send_message(apart_list)


def print_apart_list(apartments):
    text = ""

    for apartment in apartments:
        name = apartment[0]
        price = apartment[1]
        per_price = apartment[2]
        # date = apartment[3]
        text += f'{name}:{price}만원(평당{per_price}만원)\n'

    return text
