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

from mysite.weather import get_today_weather
from config import (
    STATIC_TMP,
    IMGUR_CLIENT_ID,
    IMGUR_CLIENT_SECRET,
    IMGUR_ALBUM_ID,
    IMGUR_ACCESS_TOKEN,
    IMGUR_REFRESH_TOKEN,
    IMGUR_ACCOUNT_USERNAME,
    app,
    FROM_APP,
    TAROT_FASTAPI,
    handler,
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


@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApiBlob(api_client)
        content = line_bot_api.get_message_content(message_id=event.message.id)
        f_path = os.path.join(STATIC_TMP, "tmp.jpg")

        image_io = io.BytesIO(content)
        image = Image.open(image_io)
        image.save(f_path)

        client = Imgur(
            {
                "client_id": IMGUR_CLIENT_ID,
                "client_secret": IMGUR_CLIENT_SECRET,
                "access_token": IMGUR_ACCESS_TOKEN,
                "refresh_token": IMGUR_REFRESH_TOKEN,
                "account_username": IMGUR_ACCOUNT_USERNAME,
            }
        )
        r = client.image_upload(
            filename=f_path,
            title="title_{}".format(datetime.now().strftime("%Y%m%d%H%S")),
            description="desc",
            album=IMGUR_ALBUM_ID,
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
                        TextMessage(text=f"Image Link: {link}, Preview:"),
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
            get_today_weather(FROM_APP, line_bot_api, event=event)
        elif text.lower().find("tarot") > -1:
            r = requests.get(f"{TAROT_FASTAPI}akasha/")
            if r.status_code == 200:
                resp = r.json()
                img_url = resp.get("link")
                app.logger.warning(img_url)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[
                            ImageMessage(
                                original_content_url=img_url,
                                preview_image_url=img_url,
                            ),
                        ],
                    )
                )

        else:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=event.message.text)],
                )
            )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port)
