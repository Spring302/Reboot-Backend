import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from rec.utils.trans import change_currency_language

# TODO: update https://ducj.tistory.com/157


class Cron():

    def crawling_rec(self):

        now = str(datetime.now().date())
        dic = {'Date': [], 'Name': [], 'Price': [], 'PerPrice': []}

        # 브라우저 생성
        def set_chrome_driver():
            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            # options.add_argument("headless")
            browser = webdriver.Chrome(service=Service(
                ChromeDriverManager().install()), options=options)
            return browser

        browser = set_chrome_driver()

        # 웹사이트 열기
        browser.get('https://new.land.naver.com/')

        time.sleep(1)

        search_list = ['빛가람혁신도시중흥S-클래스센트럴1차', '빛가람중흥S-클래스센트럴2차',
                       '빛가람우미린', '이노시티애시앙', '빛가람동루멘하임', '나주역자이리버파크']

        for apartment in search_list:
            # 검색창 클릭
            search = browser.find_element(By.CSS_SELECTOR, '#search_input')
            search.click()
            search.send_keys(apartment)
            search.send_keys(Keys.ENTER)

            time.sleep(3)

            # 거래방식
            transaction_style_el = browser.find_element(
                By.CSS_SELECTOR,
                '#complexOverviewList > div.list_contents > div.list_fixed > div.list_filter > div > div:nth-child(1) > button > span')
            transaction_style_el.click()

            time.sleep(0.5)

            # 매매
            sale_real_estate = browser.find_element(
                By.CSS_SELECTOR,
                '#complexOverviewList > div.list_contents > div.list_fixed > div.list_filter > div > div:nth-child(1) > div > div > ul > li:nth-child(2) > label')
            sale_real_estate.click()

            time.sleep(0.1)

            # 거래방식 창 닫기
            sale_real_estate = browser.find_element(
                By.CSS_SELECTOR,
                '#complexOverviewList > div.list_contents > div.list_fixed > div.list_filter > div > div:nth-child(1) > div > button > i')
            sale_real_estate.click()

            time.sleep(0.1)

            # 낮은가격순
            order_by_lowest_price = browser.find_element(
                By.CSS_SELECTOR, '#complexOverviewList > div.list_contents > div.list_fixed > div.sorting > a:nth-child(3)')
            order_by_lowest_price.click()

            time.sleep(1)

            # 최저가
            lowest_price_text = browser.find_element(
                By.CSS_SELECTOR, '#articleListArea > div:nth-child(1) > div > a')

            lowest_price_text.click()

            time.sleep(2)

            # 매매3억 5,000(1,220만원/3.3㎡)
            lowest_price = browser.find_element(
                By.CSS_SELECTOR, '#ct > div.map_wrap > div.detail_panel > div > div.detail_contents_inner > div.detail_fixed > div.main_info_area > div.info_article_price').text

            price, per_price = lowest_price.split("(")
            price = price[2:]
            per_price = per_price[:-8]
            per_price = per_price.replace(",", "")

            dic['Date'].append(now)  # 날짜
            dic['Name'].append(apartment)  # 아파트명
            dic['Price'].append(price)  # 최저가
            dic['PerPrice'].append(per_price)  # 평단가(3.3/m2)

            time.sleep(2)
            print(dic)
        return dic

    def crawling_rec_tuple(apart_list):
        now = str(datetime.now().date())
        response = []

        # 브라우저 생성
        def set_chrome_driver():
            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            # backgound options
            # options.add_argument("headless")
            browser = webdriver.Chrome(service=Service(
                ChromeDriverManager().install()), options=options)
            return browser

        browser = set_chrome_driver()

        # 웹사이트 열기
        browser.get('https://new.land.naver.com/')

        time.sleep(1)

        for apart in apart_list:
            print(f"search - {apart[1]}")
            price_info = {}
            # 검색창 클릭
            search = browser.find_element(By.CSS_SELECTOR, '#search_input')
            search.click()
            search.send_keys(apart[1])
            search.send_keys(Keys.ENTER)
            time.sleep(3)

            # 거래방식
            transaction_style_el = browser.find_element(
                By.CSS_SELECTOR,
                '#complexOverviewList > div.list_contents > div.list_fixed > div.list_filter > div > div:nth-child(1) > button > span')
            transaction_style_el.click()
            time.sleep(0.5)

            # 매매
            sale_real_estate = browser.find_element(
                By.CSS_SELECTOR,
                '#complexOverviewList > div.list_contents > div.list_fixed > div.list_filter > div > div:nth-child(1) > div > div > ul > li:nth-child(2)')
            sale_real_estate.click()
            time.sleep(0.1)

            # # 전세
            # sale_real_estate = browser.find_element(
            #     By.CSS_SELECTOR,
            #     '#complexOverviewList > div.list_contents > div.list_fixed > div.list_filter > div > div:nth-child(1) > div > div > ul > li:nth-child(3)')
            # sale_real_estate.click()
            # time.sleep(0.1)

            # 거래방식 창 닫기
            sale_real_estate = browser.find_element(
                By.CSS_SELECTOR,
                '#complexOverviewList > div.list_contents > div.list_fixed > div.list_filter > div > div:nth-child(1) > div > button > i')
            sale_real_estate.click()
            time.sleep(0.1)

            # 낮은가격순
            order_by_lowest_price = browser.find_element(
                By.CSS_SELECTOR, '#complexOverviewList > div.list_contents > div.list_fixed > div.sorting > a:nth-child(3)')
            order_by_lowest_price.click()
            time.sleep(1)

            # 최저가
            lowest_price_text = browser.find_element(
                By.CSS_SELECTOR, '#articleListArea > div:nth-child(1) > div > a.item_link > div.item_title')
            lowest_price_text.click()
            time.sleep(2)

            # 매매3억 5,000(1,220만원/3.3㎡)
            lowest_price = browser.find_element(
                By.CSS_SELECTOR, '#ct > div.map_wrap > div.detail_panel > div > div.detail_contents_inner > div.detail_fixed > div.main_info_area > div.info_article_price').text

            price, per_price = lowest_price.split("(")
            price = price[2:]
            per_price = per_price[:-8]
            per_price = per_price.replace(",", "")

            print(f"price: {price}, per_price: {per_price}")

            price_info['apart'] = apart[0]  # 아파트 id
            price_info['date'] = now  # 날짜
            price_info['name'] = apart[1]  # 아파트명
            price_info['price'] = change_currency_language(price)  # 최저가
            price_info['per_price'] = int(per_price)  # 평단가(3.3/m2)

            response.append(price_info)
        return response

    def crawling_rec_api(apart_list, transaction_style):
        now = str(datetime.now().date())
        response = []

        # 브라우저 생성
        def set_chrome_driver():
            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            # backgound options
            # options.add_argument("headless")
            browser = webdriver.Chrome(service=Service(
                ChromeDriverManager().install()), options=options)
            return browser

        browser = set_chrome_driver()

        # 웹사이트 열기
        browser.get('https://new.land.naver.com/')

        time.sleep(1)
        for apart in apart_list:
            print(f"search - {apart['name']}")
            price_info = {}
            # 검색창 클릭
            search = browser.find_element(By.CSS_SELECTOR, '#search_input')
            search.click()
            search.send_keys(apart['name'])
            search.send_keys(Keys.ENTER)
            time.sleep(3)

            # 거래방식
            transaction_style_el = browser.find_element(
                By.CSS_SELECTOR,
                '#complexOverviewList > div.list_contents > div.list_fixed > div.list_filter > div > div:nth-child(1) > button > span')
            transaction_style_el.click()
            time.sleep(0.5)
            
            if transaction_style == "매매":
                # 매매
                sale_real_estate = browser.find_element(
                    By.CSS_SELECTOR,
                    '#complexOverviewList > div.list_contents > div.list_fixed > div.list_filter > div > div:nth-child(1) > div > div > ul > li:nth-child(2)')
                sale_real_estate.click()
                time.sleep(0.1)
            else:
                # 전세
                sale_real_estate = browser.find_element(
                    By.CSS_SELECTOR,
                    '#complexOverviewList > div.list_contents > div.list_fixed > div.list_filter > div > div:nth-child(1) > div > div > ul > li:nth-child(3)')
                sale_real_estate.click()
                time.sleep(0.1)

            # 거래방식 창 닫기
            sale_real_estate = browser.find_element(
                By.CSS_SELECTOR,
                '#complexOverviewList > div.list_contents > div.list_fixed > div.list_filter > div > div:nth-child(1) > div > button > i')
            sale_real_estate.click()
            time.sleep(0.1)

            # 낮은가격순
            order_by_lowest_price = browser.find_element(
                By.CSS_SELECTOR, '#complexOverviewList > div.list_contents > div.list_fixed > div.sorting > a:nth-child(3)')
            order_by_lowest_price.click()
            time.sleep(1)

            # 최저가
            lowest_price_text = browser.find_element(
                By.CSS_SELECTOR, '#articleListArea > div:nth-child(1) > div > a.item_link > div.item_title')
            lowest_price_text.click()
            time.sleep(2)
            # 매매3억 5,000(1,220만원/3.3㎡)
            lowest_price = browser.find_element(
                By.CSS_SELECTOR, '#ct > div.map_wrap > div.detail_panel > div > div.detail_contents_inner > div.detail_fixed > div.main_info_area > div.info_article_price').text

            price, per_price = lowest_price.split("(")
            price = price[2:]
            per_price = per_price[:-8]
            per_price = per_price.replace(",", "")

            print(f"price: {price}, per_price: {per_price}")

            price_info['apart'] = apart['id']  # 아파트 id
            price_info['date'] = now  # 날짜
            price_info['name'] = apart['name']  # 아파트명
            price_info['transaction_style'] = transaction_style
            price_info['price'] = change_currency_language(price)  # 최저가
            price_info['per_price'] = int(per_price)  # 평단가(3.3/m2)

            response.append(price_info)
        return response

    def make_csv(self):
        df = pd.DataFrame(self.crawling_rec())
        df.to_csv('/data/rec/rec.csv', index=False, mode='a', encoding='utf-8-sig', header=False)

    def make_json(self):
        csv_data = pd.read_csv('/data/rec/rec.csv')
        csv_data.to_json('/data/rec/rec.json', orient='records', force_ascii=False)
