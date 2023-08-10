from datetime import datetime, timedelta

from linebot.v3.messaging import (
    PushMessageRequest,
    ApiClient,
    MessagingApi,
    StickerMessage,
)

from config import configuration, dict_city


def get_city(text: str) -> str:

    city = "台北市"
    if "新北" in text:
        city = "新北市"
    elif "基隆" in text:
        city = "基隆市"
    elif "花蓮" in text:
        city = "花蓮縣"
    elif "宜蘭" in text:
        city = "宜蘭縣"
    elif "金門" in text:
        city = "金門縣"
    elif "澎湖" in text:
        city = "澎湖縣"
    elif "台南" in text:
        city = "台南市"
    elif "高雄" in text:
        city = "高雄市"
    elif "嘉義縣" in text:
        city = "嘉義縣"
    elif "嘉義市" in text or "嘉義" in text:
        city = "嘉義市"
    elif "苗栗" in text:
        city = "苗栗縣"
    elif "台中" in text or "臺中" in text:
        city = "台中市"
    elif "桃園" in text:
        city = "桃園市"
    elif "新竹縣" in text:
        city = "新竹縣"
    elif "新竹市" in text or "新竹" in text:
        city = "新竹市"
    elif "屏東" in text:
        city = "屏東縣"
    elif "南投" in text:
        city = "南投縣"
    elif "臺東" in text or "台東" in text:
        city = "臺東縣"
    elif "彰化" in text:
        city = "彰化縣"
    elif "雲林" in text:
        city = "雲林縣"
    elif "連江" in text:
        city = "連江縣"

    return city


class WeatherDataParser:
    @classmethod
    def _process_36hrs(cls, city, data):
        time_start, wx, temper = [], [], []

        issued = data["cwbopendata"]["dataset"]["datasetInfo"]["issueTime"]

        location = data["cwbopendata"]["dataset"]["location"]

        city_weather = location[dict_city.get(city, 0)]
        weather_elements = city_weather["weatherElement"]
        w_desc_time = weather_elements[0]["time"]
        max_t = weather_elements[1]
        min_t = weather_elements[2]

        for ele in w_desc_time:
            dt_start = datetime.strptime(ele["startTime"], "%Y-%m-%dT%H:%M:%S%z")
            time_start.append(dt_start)

        for i in range(len(w_desc_time) - 1):
            wx.append(w_desc_time[i]["parameter"]["parameterName"])
            t_msg = "{}°C ~ {}°C".format(
                min_t["time"][i]["parameter"]["parameterName"],
                max_t["time"][i]["parameter"]["parameterName"],
            )
            temper.append(t_msg)

        return time_start, wx, temper, issued

    @classmethod
    def _process_helper(cls, data):

        location = data["cwbopendata"]["dataset"]["location"]["locationName"]
        desc = data["cwbopendata"]["dataset"]["parameterSet"]["parameter"][2][
            "parameterValue"
        ]
        return location, desc

    @classmethod
    def main(cls, city, data1, data2):

        time_start, wx, temper, issued = cls._process_36hrs(city, data1)

        loc, desc = cls._process_helper(data2)

        return FlexMessageMaker(
            **{
                "loc": loc,
                "time_start": time_start,
                "temper": temper,
                "weather": wx,
                "desc": desc,
                "issued": issued,
            }
        ).run()


class FlexMessageMaker:
    """
    weather json data class
    """

    def __init__(self, loc, time_start, temper, weather, desc, issued: str):
        self.loc = loc
        self.time_start = time_start
        self.temper = temper
        self.weather = weather
        self.desc = desc
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
        for i in range(len(self.time_start) - 1):
            start_str = self.time_start[i].strftime("%m-%d %H:%M")
            end_str = (self.time_start[i] + timedelta(hours=12)).strftime("%m-%d %H:%M")
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

        return {"type": "box", "layout": "vertical", "contents": res}

    def _make_desc_box(self):
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
                    "text": self.desc,
                    "size": "sm",
                    "color": "#8c8c8c",
                    "flex": 2,
                    "wrap": True,
                },
            ],
            "spacing": "md",
        }

    def run(self) -> dict:
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
                        "text": self.loc,
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
                            self._make_desc_box(),
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
