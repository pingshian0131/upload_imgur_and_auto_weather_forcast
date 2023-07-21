import os
import json
import random
from datetime import datetime

import requests
from flask import request, abort
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    ImageSendMessage,
    ImageMessage,
)

# from model import *
import tempfile
import errno
from imgur_python import Imgur

from mysite.weather import data_process
from config import (
    client_id,
    client_secret,
    album_id,
    access_token,
    refresh_token,
    line_bot_api,
    handler,
    account_username,
    app,
    FROM_APP,
    TAROT_FASTAPI,
)


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    bodyjson = json.loads(body)
    # app.logger.error("Request body: " + bodyjson['events'][0]['message']['text'])
    app.logger.warning("Request body: " + body)
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
            TextSendMessage(
                text="APIServerError: status={}".format(r.get("status", "None"))
            ),
        )


@handler.add(MessageEvent, message=TextMessage)
def handle_text_msg(event):
    app.logger.warning(event)
    app.logger.warning(event.message.text)
    text = event.message.text
    if "天氣" in text or "weather" in text.lower():
        data_process(FROM_APP, event=event)

    elif text.lower().find("tarot") > -1:
        data = random.randint(1, 49)
        r = requests.get(f"{TAROT_FASTAPI}akasha/{data}/")
        if r.status_code == 200:
            resp = r.json()
            img_url = resp.get("link")
            app.logger.warning(img_url)
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url=img_url, preview_image_url=img_url
                ),
            )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True, use_debugger=True, use_reloader=True)
