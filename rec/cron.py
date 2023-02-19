from django_cron import CronJobBase, Schedule
from rec.models import *        
from rec.serializers import *    
from rec.utils.cron import Cron
from datetime import datetime
from django.db import IntegrityError

class MessageTask(CronJobBase):
    RUN_EVERY_MINS = 1  # Run every hour
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'rec.message_task'    # a unique code
    def print_apart_list(self, apartments):
        text = ""
        for apartment in apartments:
            name = apartment['apart']['name']
            transaction_style = apartment['transaction_style']
            price = apartment['price']
            per_price = apartment['per_price']
            # date = apartment['date']
            text += f"{name}({transaction_style}):{price}만원(평당{per_price}만원)\n"
        return text
    
    def do(self):
        today = datetime.today().strftime("%Y-%m-%d")
        queryset = PriceInfo.objects.filter(date=today)
        serializer = PriceInfoSerializer(queryset, many=True)
        print(self.print_apart_list(serializer.data))

class SeleniumTask(CronJobBase):
    RUN_EVERY_MINS = 1  # Run every hour
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'rec.selenium_task'    # a unique code

    def do(self):

        def save_data(crawling_list):
            for info in crawling_list:
                apart_id = Apartments.objects.get(pk=info["apart"])
                price_info = PriceInfo(
                    apart=apart_id,
                    transaction_style=info["transaction_style"],
                    price=info["price"],
                    per_price=info["per_price"],
                )
            try:
                price_info.save()
            except IntegrityError as e:
                print("IntegrityError Error:", e)
        apartments = Apartments.objects.all()
        apartments_serializer = ApartmentsSerializer(apartments, many=True)
        crawling_list1 = Cron.crawling_rec_api(apartments_serializer.data, "전세")
        crawling_list2 = Cron.crawling_rec_api(apartments_serializer.data, "매매")
        save_data(crawling_list1)
        save_data(crawling_list2)
    
    def test(self):
        print("test")