import os

from flask import Flask
from flask_caching import Cache
from linebot import LineBotApi, WebhookHandler
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration

handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET", ""))

configuration = Configuration(
    access_token=os.environ.get(
        "LINE_CHANNEL_ACCESS_TOKEN",
        "",
    )
)

STATIC_TMP = os.path.join(os.path.dirname(__file__), "static", "tmp")
# imgur key
IMGUR_CLIENT_ID = os.environ.get("IMGUR_CLIENT_ID", "")
IMGUR_CLIENT_SECRET = os.environ.get("IMGUR_CLIENT_SECRET", "")
IMGUR_ALBUM_ID = os.environ.get("IMGUR_ALBUM_ID", "")
IMGUR_ACCESS_TOKEN = os.environ.get("IMGUR_ACCESS_TOKEN", "")
IMGUR_REFRESH_TOKEN = os.environ.get("IMGUR_REFRESH_TOKEN", "")
IMGUR_ACCOUNT_USERNAME = os.environ.get("IMGUR_ACCOUNT_USERNAME", "")

# opendata token
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
OPENWEATHER_TOKEN = os.environ.get("OPENWEATHER_TOKEN", "")

TAROT_FASTAPI = os.environ.get("TAROT_FASTAPI", "")

FROM_APP = 0
FROM_TASK = 1

app = Flask(__name__)

# db = SQLAlchemy()
app.config.from_mapping(flask_config)
cache = Cache(app)
