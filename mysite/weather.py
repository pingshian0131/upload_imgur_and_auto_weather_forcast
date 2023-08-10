import requests
from linebot.v3.messaging import (
    ReplyMessageRequest,
    TextMessage,
    FlexMessage,
    FlexContainer,
    PushMessageRequest,
)

from config import OPENWEATHER_URL, cache, app, FROM_APP, dict_helper
from mysite.utils import WeatherDataParser, get_city, FlexMessageMaker


def get_today_weather(_from, line_bot_api, *args, **kwargs):
    if _from == FROM_APP:
        event = kwargs["event"]
        text = event.message.text
    else:
        event = None
        text = kwargs["text"]
        user_id = kwargs["user_id"]

    city = get_city(text)

    cache_key1 = f"weather_F-C0032-001"

    # 天氣小幫手
    cache_key2 = f"helper_F-C0032-{dict_helper.get(city, '009')}"

    cache_key3 = f"img_F-D0047-089"

    # try:
    flex1 = WeatherDataParser().msg1(city, cache_key1, cache_key2, _from)
    alt_text = f"{city}天氣預報"
    flex2 = WeatherDataParser().msg2(city, cache_key3, _from)

    if _from == FROM_APP:
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    FlexMessage(
                        alt_text=alt_text, contents=FlexContainer.from_dict(flex1)
                    ),
                    FlexMessage(
                        alt_text=alt_text, contents=FlexContainer.from_dict(flex2)
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

    # except Exception as e:
    #     line_bot_api.reply_message_with_http_info(
    #         ReplyMessageRequest(
    #             reply_token=event.reply_token,
    #             messages=[TextMessage(text=str(e))],
    #         )
    #     )
