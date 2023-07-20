# LineBot 

## Function
1. Upload image to imgur album.
2. Get weather forcast from cwb opendata and reply to user.
3. Push weather forcast message to specific user.
4. Get tarot image from FastAPI.

## Before Start
- prepare your config.py
```python
from flask import Flask
from flask_caching import Cache
from linebot import LineBotApi, WebhookHandler

# imgur key
client_id = ""
client_secret = ""
album_id = ""
access_token = ""
refresh_token = ""
account_username = ""
# Channel Access Token
line_bot_api = LineBotApi("")
# Channel Secret
handler = WebhookHandler("")
# opendata token
TOKEN = ""
USER_ID = ""

flask_config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
    "SQLALCHEMY_DATABASE": "",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
}

OPENWEATHER_URL = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/"

FROM_APP = 0
FROM_TASK = 1
app = Flask(__name__)
app.config.from_mapping(flask_config)
cache = Cache(app)
```