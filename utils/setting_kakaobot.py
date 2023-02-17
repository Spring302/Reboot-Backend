import requests
import json
from pathlib import Path
import os
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# reading .env file
environ.Env.read_env(env_file=os.path.join(BASE_DIR, "./env/.env"))

REST_API_KEY = env("KAKAO_REATAPI_KEY")
# REDIRECT_URI = env("REDIRECT_URI")
REDIRECT_URI = "https://example.com/oauth"
CODE = env("KAKAO_CODE")
REFRESH_TOKEN = env("KAKAO_REFRESH_TOKEN")

url = "https://kauth.kakao.com/oauth/token"


def init_token():
    data = {
        "grant_type": "authorization_code",
        "client_id": REST_API_KEY,
        "redirect_uri": REDIRECT_URI,
        "code": CODE,
    }

    response = requests.post(url, data=data)
    tokens = response.json()

    with open("./env/kakao_token.json", "w") as kakao:
        json.dump(tokens, kakao)


def refresh_token():
    data = {
        "grant_type": "refresh_token",
        "client_id": REST_API_KEY,
        "refresh_token": REFRESH_TOKEN,
    }
    response = requests.post(url, data=data)
    tokens = response.json()
    # kakao_code.json 파일 저장
    with open("./env/kakao_refresh_token.json", "w") as fp:
        json.dump(tokens, fp)
