from datetime import datetime

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



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
