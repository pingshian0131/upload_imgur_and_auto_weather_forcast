import os

from flask import Flask
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    SourceUser,
    SourceGroup,
    SourceRoom,
    ImageSendMessage,
    TemplateSendMessage,
    ConfirmTemplate,
    MessageAction,
    ButtonsTemplate,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    URIAction,
    PostbackAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction,
    CarouselTemplate,
    CarouselColumn,
    PostbackEvent,
    StickerMessage,
    StickerSendMessage,
    LocationMessage,
    LocationSendMessage,
    ImageMessage,
    VideoMessage,
    AudioMessage,
    FileMessage,
    UnfollowEvent,
    FollowEvent,
    JoinEvent,
    LeaveEvent,
    BeaconEvent,
    FlexSendMessage,
    BubbleContainer,
    ImageComponent,
    BoxComponent,
    TextComponent,
    IconComponent,
    ButtonComponent,
    SeparatorComponent,
    QuickReply,
    QuickReplyButton,
    CarouselContainer,
)
import urllib.request
from dateutil import parser
import json
import weather
from config import line_bot_api

app = Flask(__name__)

# db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE"] = ""
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

def job():
    """
    original function is setting a scheduler on heroku server
    line bot would auto push weather forcast at 7:00 A.M. every morning
    weather forcast flex message made from weather.py
    weather data come from https://opendata.cwb.gov.tw/index
    """
    #    global scheduler
    #    scheduler.enter(60*60*24 , tell_weather(user_id))
    #    ssl._create_default_https_context = ssl._create_unverified_context
    user_id = os.getenv("user_id", "")
    token = os.getenv("token", "")
    url = (
        "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization="
        + token
        + "&format=JSON"
    )
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
    location = data["cwbopendata"]["dataset"]["location"]
    Taipei_weather = location[1]
    weather_elements = location[1]["weatherElement"]
    Wx = weather_elements[0]
    MaxT = weather_elements[1]
    MinT = weather_elements[2]
    Time_start, Time_end = [], []
    wx = []
    for i in range(len(Wx["time"])):
        t_start = Wx["time"][i]["startTime"]
        dt_start = parser.parse(t_start)
        Time_start.append(dt_start.strftime("%m/%d %H:%M"))

    maxT, minT = "", ""
    temper = []
    for i in range(len(Wx["time"])):
        if i == len(Wx["time"]) - 1:
            break
        wx.append(Wx["time"][i]["parameter"]["parameterName"])
        maxT = MaxT["time"][i]["parameter"]["parameterName"]
        minT = MinT["time"][i]["parameter"]["parameterName"]
        temper.append(minT + "°C" + " ~ " + maxT + "°C")
    url2 = (
        "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-010?Authorization="
        + token
        + "&format=JSON"
    )
    with urllib.request.urlopen(url2) as url:
        data = json.loads(url.read().decode())
    location = data["cwbopendata"]["dataset"]["location"]["locationName"]
    weather_helper = data["cwbopendata"]["dataset"]["parameterSet"]
    header = weather_helper["parameterSetName"]
    weather_elements = weather_helper["parameter"]
    comment = weather_elements[2]["parameterValue"]

    weather_obj = weather.weather_data(
        location=location, date=Time_start, temper=temper, weather=wx, comment=comment
    )
    flex_s = weather_obj.make_json()
    flex = json.loads(flex_s)

    line_bot_api.push_message(
        user_id, FlexSendMessage(alt_text="WeatherForcast", contents=flex)
    )


if __name__ == "__main__":
    job()
