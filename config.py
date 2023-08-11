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

OPENWEATHER_URL = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/"
OPENWEATHER_TOKEN = os.environ.get("OPENWEATHER_TOKEN", "")

TAROT_FASTAPI = os.environ.get("TAROT_FASTAPI", "")

FROM_APP = 0
FROM_TASK = 1

app = Flask(__name__)

# db = SQLAlchemy()
app.config.from_mapping(flask_config)
cache = Cache(app)

dict_city = {
    "台北市": 0,
    "新北市": 1,
    "基隆市": 6,
    "花蓮縣": 17,
    "宜蘭縣": 16,
    "金門縣": 20,
    "澎湖縣": 19,
    "台南市": 4,
    "高雄市": 5,
    "嘉義縣": 13,
    "嘉義市": 14,
    "苗栗縣": 9,
    "台中市": 3,
    "桃園市": 2,
    "新竹縣": 7,
    "新竹市": 8,
    "屏東縣": 15,
    "南投縣": 11,
    "臺東縣": 18,
    "彰化縣": 10,
    "雲林縣": 12,
    "連江縣": 21,
}
dict_helper = {
    "台北市": "009",
    "新北市": "010",
    "基隆市": "011",
    "花蓮縣": "012",
    "宜蘭縣": "013",
    "金門縣": "014",
    "澎湖縣": "015",
    "台南市": "016",
    "高雄市": "017",
    "嘉義縣": "018",
    "嘉義市": "019",
    "苗栗縣": "020",
    "台中市": "021",
    "桃園市": "022",
    "新竹縣": "023",
    "新竹市": "024",
    "屏東縣": "025",
    "南投縣": "026",
    "臺東縣": "027",
    "彰化縣": "028",
    "雲林縣": "029",
    "連江縣": "030",
}
dict_img = {
    "台北市": "63000000",
    "新北市": "65000000",
    "基隆市": "10017000",
    "花蓮縣": "10015000",
    "宜蘭縣": "10002000",
    "金門縣": "09020000",
    "澎湖縣": "10016000",
    "台南市": "67000000",
    "高雄市": "64000000",
    "嘉義縣": "10010000",
    "嘉義市": "10020000",
    "苗栗縣": "10005000",
    "台中市": "66000000",
    "桃園市": "68000000",
    "新竹縣": "10004000",
    "新竹市": "10018000",
    "屏東縣": "10013000",
    "南投縣": "10008000",
    "臺東縣": "10014000",
    "彰化縣": "10007000",
    "雲林縣": "10009000",
    "連江縣": "09007000",
}

weather_pic = {
    "01": "☀️",
    "02": "🌤️",
    "03": "⛅️",
    "04": "⛅️",
    "05": "🌥️",
    "06": "🌥️",
    "07": "☁️",
    "08": "🌦️",
    "09": "🌧️",
    "10": "🌧️",
    "11": "🌧️",
    "12": "🌧️",
    "13": "🌧️",
    "14": "☔️",
    "15": "⛈️",
    "16": "⛈️",
    "17": "⛈️",
    "18": "⛈️",
    "19": "🌦️",
    "20": "🌧️",
    "21": "🌦️",
    "22": "⛈️",
    "23": "🌨️",
    "24": "💨",
    "25": "💨",
    "26": "🌥️",
    "27": "☁️",
    "28": "💨",
    "29": "🌧️",
    "30": "🌦️",
    "31": "🌧️",
    "42": "❄️",
}
