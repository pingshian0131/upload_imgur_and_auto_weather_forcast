import urllib
from datetime import datetime

from dateutil import parser
from flask import Flask, request, abort
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
    # SpacerComponent,
    IconComponent,
    ButtonComponent,
    SeparatorComponent,
    QuickReply,
    QuickReplyButton,
    CarouselContainer,
)
import os
import json

# from model import *
import tempfile
import errno
from imgur_python import Imgur

import weather
from config import (
    client_id,
    client_secret,
    album_id,
    access_token,
    refresh_token,
    line_bot_api,
    handler,
    account_username,
)
import sys

app = Flask(__name__)

# db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE"] = ""
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    bodyjson = json.loads(body)
    # app.logger.error("Request body: " + bodyjson['events'][0]['message']['text'])
    app.logger.info("Request body: " + body)
    # insertdata
    print("-----in----------")
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


static_tmp_path = os.path.join(os.path.dirname(__file__), "static", "tmp")

# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise


@handler.add(MessageEvent, message=ImageMessage)
def handle_msg_sticker(event):
    """
    ImageMessage auto upload to imgur and reply image url
    """
    make_static_tmp_dir()
    if isinstance(event.message, ImageMessage):
        ext = "jpg"
    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(
        dir=static_tmp_path, prefix=ext + "-", delete=False
    ) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + "." + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)
    client = Imgur(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "account_username": account_username,
        }
    )
    path = os.path.join("static", "tmp", dist_name)
    r = client.image_upload(
        filename=path,
        title="title_{}".format(datetime.now().strftime("%Y%m%d%H%S")),
        description="desc",
        album=album_id,
        disable_audio=1,
    )
    os.remove(path)
    if r.get("status") == 200:
        link = r["response"]["data"]["link"]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="You can find image here: {0}".format(link)),
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="APIServerError: status={}".format(r.get("status", "None"))),
        )


@handler.add(MessageEvent, message=TextMessage)
def handle_text_msg(event):
    app.logger.warning(event)
    app.logger.warning(event.message.text)
    if event.message.text == "天氣":
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

        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="WeatherForcast", contents=flex),
        )





if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
