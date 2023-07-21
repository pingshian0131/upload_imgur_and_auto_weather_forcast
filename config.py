import os

from flask import Flask
from flask_caching import Cache
from linebot import LineBotApi, WebhookHandler

# imgur key
client_id = os.environ("client_id", "")
client_secret = os.environ("client_secret", "")
album_id = os.environ("album_id", "")
access_token = os.environ("access_token", "")
refresh_token = os.environ("refresh_token", "")
account_username = os.environ("account_username", "")
# Channel Access Token
line_bot_api = LineBotApi(
    os.environ("line_bot_api", "")
)
# Channel Secret
handler = WebhookHandler(os.environ("webhook", ""))
# opendata token
TOKEN = os.environ("TOKEN", "")
USER_ID = os.environ("USER_ID", "")

flask_config = {
    "DEBUG": os.environ("DEBUG", ""),  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
    "SQLALCHEMY_DATABASE": "",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
}

OPENWEATHER_URL = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/"

TAROT_FASTAPI = os.environ("TAROT_FASTAPI", "")

FROM_APP = 0
FROM_TASK = 1

app = Flask(__name__)

# db = SQLAlchemy()
app.config.from_mapping(flask_config)
cache = Cache(app)
