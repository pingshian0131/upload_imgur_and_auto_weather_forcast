import os
import json
from datetime import datetime

import io
from PIL import Image

import requests
from flask import request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import AsyncMessagingApiBlob, MessagingApiBlob
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent,
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage,
)

# from model import *
import tempfile
import errno
from imgur_python import Imgur
from linebot.v3.webhooks import TextMessageContent

from mysite.weather import today_weather
from config import (
    client_id,
    client_secret,
    album_id,
    access_token,
    refresh_token,
    handler,
    account_username,
    app,
    FROM_APP,
    TAROT_FASTAPI,
    configuration,
)


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

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


@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApiBlob(api_client)
        content = line_bot_api.get_message_content(message_id=event.message.id)
        f_path = os.path.join(static_tmp_path, "tmp.jpg")

        image_io = io.BytesIO(content)
        image = Image.open(image_io)
        image.save(f_path)

        client = Imgur(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "account_username": account_username,
            }
        )
        r = client.image_upload(
            filename=f_path,
            title="title_{}".format(datetime.now().strftime("%Y%m%d%H%S")),
            description="desc",
            album=album_id,
            disable_audio=1,
        )
        os.remove(f_path)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        if r.get("status") == 200:
            link = r["response"]["data"]["link"]
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        TextMessage(text="You can find image here: {0}".format(link)),
                        ImageMessage(
                            original_content_url=link,
                            preview_image_url=link,
                        ),
                    ],
                )
            )

        else:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        TextMessage(
                            text="APIServerError: status={}".format(
                                r.get("status", "None")
                            )
                        )
                    ],
                )
            )


@handler.add(MessageEvent, message=TextMessageContent)
def message_text(event):
    app.logger.warning(event.source.user_id)
    app.logger.warning(event.message.text)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        text = event.message.text
        if "天氣" in text or "weather" in text.lower():
            today_weather(FROM_APP, line_bot_api, event=event)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)],
            )
        )



# @handler.add(MessageEvent, message=TextMessage)
# def handle_text_msg(event):
#     app.logger.warning(event)
#     app.logger.warning(event.message.text)
#     text = event.message.text
#     if "天氣" in text or "weather" in text.lower():
#         today_weather(FROM_APP, event=event)
#
#     elif text.lower().find("tarot") > -1:
#         r = requests.get(f"{TAROT_FASTAPI}akasha/")
#         if r.status_code == 200:
#             resp = r.json()
#             img_url = resp.get("link")
#             app.logger.warning(img_url)
#             line_bot_api.reply_message(
#                 event.reply_token,
#                 ImageSendMessage(
#                     original_content_url=img_url, preview_image_url=img_url
#                 ),
#             )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port)
