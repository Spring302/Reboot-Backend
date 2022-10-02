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
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)
REST_API_KEY = env('KAKAO_REATAPI_KEY')
# REDIRECT_URI = env('REDIRECT_URI')
REDIRECT_URI = "https://example.com/oauth"
CODE = env('KAKAO_CODE')
url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type": "authorization_code",
    "client_id": REST_API_KEY,
    "redirect_uri": REDIRECT_URI,
    "code": CODE
}

response = requests.post(url, data=data)
tokens = response.json()

with open("token.json", "w") as kakao:
    json.dump(tokens, kakao)
