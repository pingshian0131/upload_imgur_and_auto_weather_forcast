from datetime import datetime, timedelta

from linebot.v3.messaging import (
    PushMessageRequest,
    ApiClient,
    MessagingApi,
    StickerMessage,
)

from config import configuration


class WeatherDataParser:
    """
    weather json data class
    """

    def __init__(self, location, date, temper, weather, comment, issued: str):
        self.location = location
        self.date = date
        self.temper = temper
        self.weather = weather
        self.comment = comment
        self.issued = issued

    def _make_weather_box(self):
        res = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "天氣",
                        "gravity": "center",
                        "size": "sm",
                        "align": "center",
                        "flex": 1,
                    }
                ],
                "height": "30px",
            }
        ]
        for i in range(len(self.weather)):
            res.append(
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [{"type": "filler"}],
                    "backgroundColor": "#0367D3",
                    "height": "2px",
                }
            )
            res.append(
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": self.weather[i],
                            "size": "sm",
                            "color": "#8c8c8c",
                            "wrap": True,
                            "gravity": "center",
                            "align": "center",
                        }
                    ],
                    "height": "70px",
                    "justifyContent": "center",
                }
            )

        print({"type": "box", "layout": "vertical", "contents": res})
        return {"type": "box", "layout": "vertical", "contents": res}

    def _make_dates_box(self):
        res = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "時間",
                        "gravity": "center",
                        "size": "sm",
                        "align": "center",
                        "flex": 1,
                    }
                ],
                "height": "30px",
            }
        ]
        for i in range(len(self.date) - 1):
            start_str = self.date[i].strftime("%m-%d %H:%M")
            end_str = (self.date[i] + timedelta(hours=12)).strftime("%m-%d %H:%M")
            res.append(
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [{"type": "filler"}],
                    "backgroundColor": "#0367D3",
                    "height": "2px",
                }
            )
            res.append(
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": start_str,
                                    "size": "sm",
                                    "color": "#8c8c8c",
                                    "flex": 2,
                                    "align": "center",
                                    "gravity": "center",
                                    "wrap": True,
                                },
                                {
                                    "type": "text",
                                    "text": end_str,
                                    "size": "sm",
                                    "color": "#8c8c8c",
                                    "flex": 2,
                                    "align": "center",
                                    "gravity": "center",
                                    "wrap": True,
                                },
                            ],
                        }
                    ],
                    "height": "70px",
                }
            )

        print({"type": "box", "layout": "vertical", "contents": res})
        return {"type": "box", "layout": "vertical", "contents": res}

    def _make_temper_box(self):
        res = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "氣溫",
                        "gravity": "center",
                        "size": "sm",
                        "align": "center",
                        "flex": 1,
                    }
                ],
                "height": "30px",
            }
        ]
        for i in range(len(self.temper)):
            res.append(
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [{"type": "filler"}],
                    "backgroundColor": "#0367D3",
                    "height": "2px",
                }
            )
            res.append(
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": self.temper[i],
                            "size": "md",
                            "color": "#8c8c8c",
                            "flex": 2,
                            "align": "center",
                            "gravity": "center",
                            "wrap": True,
                        }
                    ],
                    "height": "70px",
                }
            )

        print({"type": "box", "layout": "vertical", "contents": res})
        return {"type": "box", "layout": "vertical", "contents": res}

    def _make_comment_box(self):
        return {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{"type": "filler"}],
                    "cornerRadius": "30px",
                    "width": "12px",
                    "height": "12px",
                    "borderWidth": "2px",
                    "borderColor": "#6486E3",
                },
                {
                    "type": "text",
                    "text": self.comment,
                    "size": "sm",
                    "color": "#8c8c8c",
                    "flex": 2,
                    "wrap": True,
                },
            ],
            "spacing": "md",
        }

    def make_json(self) -> dict:
        dt = datetime.strptime(self.issued, "%Y-%m-%dT%H:%M:%S%z")
        last_update_time = f"最後更新時間: {dt.strftime('%Y-%m-%d %H:%M')}"
        return {
            "type": "bubble",
            "size": "giga",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "天氣", "color": "#ffffff66", "size": "sm"},
                    {
                        "type": "text",
                        "text": self.location,
                        "color": "#ffffff",
                        "size": "xl",
                        "weight": "bold",
                    },
                ],
                "paddingAll": "20px",
                "backgroundColor": "#0367D3",
                "paddingTop": "22px",
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "天氣概況",
                                        "gravity": "center",
                                        "size": "sm",
                                    }
                                ],
                                "flex": 1,
                            },
                            self._make_comment_box(),
                        ],
                        "spacing": "md",
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "今明24小時天氣預報預報", "size": "sm"}
                        ],
                        "flex": 1,
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            self._make_dates_box(),
                            self._make_temper_box(),
                            self._make_weather_box(),
                        ],
                    },
                    {
                        "type": "text",
                        "text": last_update_time,
                        "color": "#b7b7b7",
                        "size": "xs",
                        "align": "end",
                    },
                ],
                "spacing": "xl",
            },
        }


def push_sticker_yo(user_id):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.push_message(
            PushMessageRequest(
                to=user_id,
                messages=[
                    StickerMessage(
                        package_id="446",
                        sticker_id="1989",
                    ),
                    StickerMessage(
                        package_id="789",
                        sticker_id="10857",
                    ),
                    StickerMessage(
                        package_id="6325",
                        sticker_id="10979907",
                    ),
                    StickerMessage(
                        package_id="6325",
                        sticker_id="10979910",
                    ),
                ],
            )
        )
