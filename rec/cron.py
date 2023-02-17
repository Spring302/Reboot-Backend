from django_cron import CronJobBase, Schedule
from rec.models import *        
from rec.serializers import *    
from rec.utils.cron import Cron
from datetime import datetime

class MessageTask(CronJobBase):
    RUN_EVERY_MINS = 1  # Run every hour
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'rec.message_task'    # a unique code

    def print_apart_list(self, apartments):
        text = ""
        for apartment in apartments:
            name = apartment[0]
            transaction_style = apartment[1]
            price = apartment[2]
            per_price = apartment[3]
            # date = apartment[4]
            text += f"{name}({transaction_style}):{price}만원(평당{per_price}만원)\n"
        return text
    
    def do(self):
        today = datetime.today().strftime("%Y-%m-%d")
        queryset = PriceInfo.objects.filter(date=today)
        serializer = PriceInfoSerializer(queryset.data, many=True)
        print(serializer.data)


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
                price_info.save()

        apartments = Apartments.objects.all()
        apartments_serializer = ApartmentsSerializer(apartments, many=True)
        crawling_list1 = Cron.crawling_rec_api(apartments_serializer.data, "전세")
        crawling_list2 = Cron.crawling_rec_api(apartments_serializer.data, "매매")
        save_data(crawling_list1)
        save_data(crawling_list2)
    
    def test(self):
        print("test")