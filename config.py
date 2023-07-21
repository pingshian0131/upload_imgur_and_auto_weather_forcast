import os

from flask import Flask
from flask_caching import Cache
from linebot import LineBotApi, WebhookHandler

# imgur key
client_id = os.environ.get("client_id", "")
client_secret = os.environ.get("client_secret", "")
album_id = os.environ.get("album_id", "")
access_token = os.environ.get("access_token", "")
refresh_token = os.environ.get("refresh_token", "")
account_username = os.environ.get("account_username", "")
# Channel Access Token
line_bot_api = LineBotApi(
    os.environ.get("line_bot_api", "")
)
# Channel Secret
handler = WebhookHandler(os.environ.get("webhook", ""))
# opendata token
TOKEN = os.environ.get("TOKEN", "")
USER1 = os.environ.get("USER1", "")
USER2 = os.environ.get("USER2", "")

flask_config = {
    "DEBUG": os.environ.get("DEBUG", ""),  # some Flask specific configs
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
