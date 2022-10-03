import requests
import json
from utils.setting_kakaobot import refresh_token


class Kakaobot:

    def send_message(self, text):

        # 발행한 토큰 불러오기
        with open("./env/kakao_refresh_token.json", "r") as kakao:
            tokens = json.load(kakao)

        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

        headers = {
            "Authorization": "Bearer " + tokens["access_token"]
        }
        data = {
            'object_type': 'text',
            'text': str(text),
            'link': {
                'web_url': 'https://developers.kakao.com',
                'mobile_web_url': 'https://developers.kakao.com'
            },
            'button_title': '키워드'
        }

        data = {'template_object': json.dumps(data)}
        response = requests.post(url, headers=headers, data=data)
        if response.json().get('result_code') == 0:
            print('메시지를 성공적으로 보냈습니다.')
        else:
            print('메시지를 성공적으로 보내지 못했습니다. 잠시 후 다시 시도하세요. 오류메시지 : ' + str(response.json()))
            refresh_token()
