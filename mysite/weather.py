import requests
from linebot.v3.messaging import (
    ReplyMessageRequest,
    TextMessage,
    FlexMessage,
    FlexContainer,
    PushMessageRequest,
)

from config import OPENWEATHER_URL, cache, app, FROM_APP, dict_helper
from config import OPENWEATHER_TOKEN as TOKEN
from mysite.utils import WeatherDataParser, get_city


def get_today_weather(_from, line_bot_api, *args, **kwargs):
    if _from == FROM_APP:
        event = kwargs["event"]
        text = event.message.text
    else:
        event = None
        text = kwargs["text"]
        user_id = kwargs["user_id"]

    city = get_city(text)

    cache_key = f"weather_F-C0032-001"
    data1 = cache.get(cache_key)
    if not data1:
        url = f"{OPENWEATHER_URL}F-C0032-001?Authorization={TOKEN}&format=JSON"
        r = requests.get(url)
        if r.status_code == 200:
            data1 = r.json()
            cache.set(cache_key, data1, 60 * 60)
            app.logger.warning(data1)
        else:
            if _from == FROM_APP:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[
                            TextMessage(
                                text="APIServerError: status={}".format(r.status_code)
                            )
                        ],
                    )
                )
            else:
                app.logger.error("APIServerError: status={}".format(r.status_code))

    # 天氣小幫手
    cache_key = f"helper_F-C0032-{dict_helper.get(city, '009')}"
    data2 = cache.get(cache_key)
    if not data2:
        url = f"{OPENWEATHER_URL}F-C0032-{dict_helper.get(city, '009')}?Authorization={TOKEN}&format=JSON"
        r = requests.get(url)
        if r.status_code == 200:
            data2 = r.json()
            cache.set(cache_key, data2, 60 * 60)
            app.logger.warning(data2)
        else:
            if _from == FROM_APP:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[
                            TextMessage(
                                text="APIServerError: status={}".format(r.status_code)
                            )
                        ],
                    )
                )
            else:
                app.logger.error("APIServerError: status={}".format(r.status_code))

    flex = WeatherDataParser().main(city, data1, data2)
    alt_text = f"{city}天氣預報"

    if _from == FROM_APP:
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    FlexMessage(
                        alt_text=alt_text, contents=FlexContainer.from_dict(flex)
                    )
                ],
            )
        )

    else:
        line_bot_api.push_message(
            PushMessageRequest(
                to=user_id,
                messages=[
                    FlexMessage(
                        alt_text=alt_text, contents=FlexContainer.from_dict(flex)
                    )
                ],
            )
        )
