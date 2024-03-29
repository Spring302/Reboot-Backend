from slack_sdk.errors import SlackApiError
from slack_sdk import WebClient
import logging
import os

# logging.basicConfig(level=logging.DEBUG)

SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

CHANNEL_NAME = "test"
query = "슬랙 봇 테스트"


class SlackAPI:
    """
    슬랙 API 핸들러
    """

    def __init__(self):
        try:
            # 슬랙 클라이언트 인스턴스 생성
            self.client = WebClient(SLACK_TOKEN)
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'

    def get_channel_id(self, channel_name):
        """
        슬랙 채널ID 조회
        """
        # conversations_list() 메서드 호출
        result = self.client.conversations_list()
        # 채널 정보 딕셔너리 리스트
        channels = result.data['channels']
        # 채널 명이 'test'인 채널 딕셔너리 쿼리
        channel = list(filter(lambda c: c["name"] == channel_name, channels))[0]
        # 채널ID 파싱
        channel_id = channel["id"]
        return channel_id

    def get_message_ts(self, channel_id, query):
        """
        슬랙 채널 내 메세지 조회
        """
        # conversations_history() 메서드 호출
        result = self.client.conversations_history(channel=channel_id)
        # 채널 내 메세지 정보 딕셔너리 리스트
        messages = result.data['messages']
        # 채널 내 메세지가 query와 일치하는 메세지 딕셔너리 쿼리
        message = list(filter(lambda m: m["text"] == query, messages))[0]
        # 해당 메세지ts 파싱
        message_ts = message["ts"]
        return message_ts

    def post_thread_message(self, channel_id, message_ts, text):
        """
        슬랙 채널 내 메세지의 Thread에 댓글 달기
        """
        # chat_postMessage() 메서드 호출
        result = self.client.chat_postMessage(
            channel=channel_id,
            text=text,
            thread_ts=message_ts
        )
        return result

    def send_message(self, text):
        # 채널ID 파싱
        channel_id = self.get_channel_id(CHANNEL_NAME)

        self.client.chat_postMessage(
            channel=channel_id,
            text=text,
        )
