import os

from flask import Flask
from flask_caching import Cache
from linebot import LineBotApi, WebhookHandler
from linebot.v3 import (
     WebhookHandler
)
from linebot.v3.messaging import Configuration

handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET", ""))

configuration = Configuration(
    access_token=os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "6J7NNoHty3+DlK+dtoAzHTZB89KKjCZtorOe1iaEu6zitlnCnkFcdQtYTWXkhWMaaMyxzCiiLgVQK016rdR1D9JfphRTIMHm4syVsl6X6PhY19KZlMBSqamvO0zpGEq1ynP6N7swrYG395ZR5OnFGQdB04t89/1O/w1cDnyilFU=")
)


# imgur key
client_id = os.environ.get("client_id", "")
client_secret = os.environ.get("client_secret", "")
album_id = os.environ.get("album_id", "")
access_token = os.environ.get("access_token", "")
refresh_token = os.environ.get("refresh_token", "")
account_username = os.environ.get("account_username", "")
# opendata token
TOKEN = os.environ.get("TOKEN", "")
USER1 = os.environ.get("USER1", "")
USER2 = os.environ.get("USER2", "")

flask_config = {
    "DEBUG": os.environ.get("DEBUG", True),  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
    "SQLALCHEMY_DATABASE": "",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
}

OPENWEATHER_URL = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/"

TAROT_FASTAPI = os.environ.get("TAROT_FASTAPI", "")

FROM_APP = 0
FROM_TASK = 1

app = Flask(__name__)

# db = SQLAlchemy()
app.config.from_mapping(flask_config)
cache = Cache(app)
