import requests
from linebot.v3.messaging import (
    ReplyMessageRequest,
    TextMessage,
    FlexMessage,
    FlexContainer,
    PushMessageRequest,
    MessagingApi,
)

from config import cache, app, FROM_APP, dict_helper
from mysite.utils import WeatherDataParser, get_city


def get_today_weather(_from, line_bot_api: MessagingApi, *args, **kwargs):
    if _from == FROM_APP:
        event = kwargs["event"]
        text = event.message.text
    else:
        event = None
        text = kwargs["text"]
        user_id = kwargs["user_id"]

    city = get_city(text)

    cache_key1 = f"weather_F-C0032-001_{city}"

    # 天氣小幫手
    cache_key2 = f"helper_F-C0032-{dict_helper.get(city, '009')}"

    cache_key3 = f"img_F-D0047-089_{city}"

    try:
        flex1 = WeatherDataParser().msg1(
            city, cache_key1, cache_key2, cache_key3, _from
        )
        app.logger.warning(flex1)
        alt_text = f"{city}天氣預報"

        if _from == FROM_APP:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        FlexMessage(
                            alt_text=alt_text, contents=FlexContainer.from_dict(flex1)
                        ),
                    ],
                )
            )

        else:
            line_bot_api.push_message(
                PushMessageRequest(
                    to=user_id,
                    messages=[
                        FlexMessage(
                            alt_text=alt_text, contents=FlexContainer.from_dict(flex1)
                        )
                    ],
                )
            )

    except Exception as e:
        if _from == FROM_APP:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=str(e))],
                )
            )
        else:
            app.logger.warning(str(e))


def query_18hrs_weather(line_bot_api: MessagingApi, event):
    city = get_city(event.message.text)
    cache_key3 = f"img_F-D0047-089_{city}"
    flex2 = WeatherDataParser().msg2(city, cache_key3, has_header=True)
    alt_text = f"{city}18小時天氣預報"
    line_bot_api.reply_message_with_http_info(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[
                FlexMessage(alt_text=alt_text, contents=FlexContainer.from_dict(flex2)),
            ],
        )
    )
