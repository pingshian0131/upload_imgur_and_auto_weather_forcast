import re
from datetime import datetime, timedelta

import requests
from linebot.v3.messaging import (
    PushMessageRequest,
    ApiClient,
    MessagingApi,
    StickerMessage,
)

from config import (
    configuration,
    cache,
    app,
    FROM_APP,
    OPENWEATHER_REST_API,
    OPENWEATHER_FILE_API,
    dict_helper,
    weather_pic,
    LAYOUT,
    SIZE,
)
from config import OPENWEATHER_TOKEN as TOKEN


def get_city(text: str) -> str:

    city = "臺北市"
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
        city = "臺南市"
    elif "高雄" in text:
        city = "高雄市"
    elif "嘉義縣" in text:
        city = "嘉義縣"
    elif "嘉義市" in text or "嘉義" in text:
        city = "嘉義市"
    elif "苗栗" in text:
        city = "苗栗縣"
    elif "台中" in text or "臺中" in text:
        city = "臺中市"
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
    def _process_36hrs(cls, city, cache_key, _from):

        loc = cache.get(cache_key)
        if not loc:
            dt = datetime.now() + timedelta(hours=25)
            url = f"{OPENWEATHER_REST_API}F-C0032-001?Authorization={TOKEN}&format=JSON&locationName={city}&timeTo={dt.strftime('%Y-%m-%dT%H:%M:%S')}"
            r = requests.get(url)
            if r.status_code == 200:
                data = r.json()
                app.logger.warning(data)
                if data.get("success") == "true":
                    records = data["records"]
                    loc = records["location"][0]
                    cache.set(cache_key, loc, 60 * 60)
                else:
                    raise Exception("data not success")
            else:
                if _from == FROM_APP:
                    raise Exception("APIServerError: status={}".format(r.status_code))

                else:
                    app.logger.error("APIServerError: status={}".format(r.status_code))
        time_start, wx, temper = [], [], []
        weather_elements = loc["weatherElement"]
        w_desc_time = weather_elements[0]["time"]
        max_t = weather_elements[4]
        min_t = weather_elements[2]

        time_start = [
            datetime.strptime(ele["startTime"], "%Y-%m-%d %H:%M:%S")
            for ele in w_desc_time
        ]

        for i in range(len(w_desc_time) - 1):
            wx.append(w_desc_time[i]["parameter"]["parameterName"])
            temper.append(
                "{}°C ~ {}°C".format(
                    min_t["time"][i]["parameter"]["parameterName"],
                    max_t["time"][i]["parameter"]["parameterName"],
                )
            )

        return time_start, wx, temper

    @classmethod
    def _process_helper(cls, city, cache_key, _from):

        data = cache.get(cache_key)
        if not data:
            url = f"{OPENWEATHER_FILE_API}F-C0032-{dict_helper.get(city, '009')}?Authorization={TOKEN}&format=JSON"
            r = requests.get(url)
            if r.status_code == 200:
                data = r.json()
                cache.set(cache_key, data, 60 * 60)
                app.logger.warning(data)
            else:
                if _from == FROM_APP:
                    raise Exception("APIServerError: status={}".format(r.status_code))

                else:
                    app.logger.error("APIServerError: status={}".format(r.status_code))

        location = data["cwbopendata"]["dataset"]["location"]["locationName"]
        desc = data["cwbopendata"]["dataset"]["parameterSet"]["parameter"][2][
            "parameterValue"
        ]
        return location, desc

    @classmethod
    def _process_18hrs(cls, city, cache_key, _from=FROM_APP):
        loc = cache.get(cache_key)
        if not loc:
            dt = datetime.now() + timedelta(hours=19)
            url = f"{OPENWEATHER_REST_API}F-D0047-089?Authorization={TOKEN}&format=JSON&locationName={city}&timeTo={dt.strftime('%Y-%m-%dT%H:%M:%S')}"
            app.logger.warning(url)
            r = requests.get(url)
            if r.status_code == 200:
                data = r.json()
                app.logger.warning(data)
                if data.get("success") == "true":
                    records = data["records"]
                    loc = records["locations"][0]["location"][0]
                    cache.set(cache_key, loc, 60 * 60)
                else:
                    raise Exception("data not success")
            else:
                if _from == FROM_APP:
                    raise Exception("APIServerError: status={}".format(r.status_code))

                else:
                    app.logger.error("APIServerError: status={}".format(r.status_code))
                    raise

        w_ele = loc["weatherElement"]
        pic_str = w_ele[1]  # 天氣現象
        temp = w_ele[3]  # 溫度
        desc = w_ele[6]  # 天氣預報綜合描述 -> 降雨機率

        w_pic = []
        dt1, dt_main = [], []
        for ele in pic_str["time"][:7]:
            dt = datetime.strptime(ele["startTime"], "%Y-%m-%d %H:%M:%S")
            dt1.append(dt)
            dt_main.append(str(dt.hour))
            w_pic.append(
                weather_pic.get(
                    ele["elementValue"][1]["value"], ele["elementValue"][1]["value"]
                )
            )

        t = []
        dt2 = []
        for ele in temp["time"][:7]:
            dt = datetime.strptime(ele["dataTime"], "%Y-%m-%d %H:%M:%S")
            dt2.append(dt)
            t.append(f"{ele['elementValue'][0]['value']}°C")

        s = []
        dt3 = []
        for ele in desc["time"][:7]:
            dt = datetime.strptime(ele["startTime"], "%Y-%m-%d %H:%M:%S")
            dt3.append(dt)

            pattern = r"降雨機率 (\d+)%"
            match = re.search(pattern, ele["elementValue"][0]["value"])

            rate = int(match.group(1)) if match else 0
            s.append(rate)

        if dt1 == dt2 == dt3:
            return city, dt_main, w_pic, t, s
        else:
            raise Exception("Error dt data")

    @classmethod
    def msg1(cls, city, cache_key1, cache_key2, cache_key3, _from):

        time_start, wx, temper = cls._process_36hrs(city, cache_key1, _from)
        loc, desc = cls._process_helper(city, cache_key2, _from)
        city, dt_main, w_pic, t, s = cls._process_18hrs(city, cache_key3)
        m = FlexMessageMaker1("bubble", "mega")
        m.run(
            loc=loc,
            time_start=time_start,
            temper=temper,
            wx=wx,
            desc=desc,
            dt_main=dt_main,
            w_pic=w_pic,
            t=t,
            s=s,
        )
        return m.flex

    @classmethod
    def msg2(cls, city, cache_key3, **kwargs):
        city, dt_main, w_pic, t, s = cls._process_18hrs(city, cache_key3)
        m = FlexMessageMaker2("bubble", "mega")
        m.run(city, dt_main, w_pic, t, s, has_header=kwargs["has_header"])
        return m.flex


class BaseFlexMessageMaker:
    def __init__(self, _type, size):
        self.flex = {
            "type": _type,
            "size": size,
        }

    @staticmethod
    def _text_compo(text: str, size=SIZE.MD.value, **kwargs):
        return {"type": "text", "text": text, "size": size, **kwargs}

    @staticmethod
    def _box_compo(layout: str, contents: list, **kwargs):
        return {"type": "box", "layout": layout, "contents": contents, **kwargs}

    @staticmethod
    def _filler():
        return {"type": "filler"}

    def _make_hour_ele(self, dt: str, pic: str, t: str, rate: int):

        if rate < 50:
            contents = [
                self._text_compo(text=dt, size=SIZE.XS.value),
                self._filler(),
                self._text_compo(text=pic, size=SIZE.LG.value),
                self._filler(),
                self._text_compo(text=t, size=SIZE.XXS.value),
            ]
        else:
            contents = [
                self._text_compo(text=dt, size=SIZE.XS.value),
                self._filler(),
                self._text_compo(text=pic, size=SIZE.LG.value),
                self._text_compo(
                    text=f"{rate}%", size=SIZE.XXS.value, **{"color": "#84C1FF"}
                ),
                self._filler(),
                self._text_compo(text=t, size=SIZE.XXS.value),
            ]

        return self._box_compo(
            layout=LAYOUT.VERTICAL.value,
            contents=contents,
            **{
                "flex": 0,
                "alignItems": "center",
            },
        )

    def _full_hour_content(
        self, dt_main: list[str], w_pic: list[str], t: list[str], s: list[int]
    ):
        return [
            self._box_compo(
                layout=LAYOUT.HORIZONTAL.value,
                contents=[
                    self._box_compo(
                        layout=LAYOUT.HORIZONTAL.value,
                        contents=[
                            self._make_hour_ele(dt_main[i], w_pic[i], t[i], s[i])
                            for i in range(len(dt_main))
                        ],
                        **{
                            "justifyContent": "space-between",
                            "backgroundColor": "#ECF5FF",
                            "paddingAll": SIZE.LG.value,
                        },
                    )
                ],
                **{
                    "spacing": SIZE.LG.value,
                    "cornerRadius": SIZE.XL.value,
                    "margin": SIZE.LG.value,
                    "height": "120px",
                },
            )
        ]

    def _header(self, *args, **kwargs):
        raise NotImplementedError

    def _body(self, *args, **kwargs):
        raise NotImplementedError

    def run(self, *args, **kwargs):
        raise NotImplementedError


class FlexMessageMaker1(BaseFlexMessageMaker):
    """
    weather json data class
    """

    def __init__(self, _type, size):
        super().__init__(_type, size)
        self.WEATHER_DATA = "天氣"
        self.DATE_DATA = "時間"
        self.TEMPER_DATA = "氣溫"
        self.MAX_DATA = 2

    def _make_data_box(self, data_type, count, **kwargs):
        res = [
            self._box_compo(
                layout=LAYOUT.HORIZONTAL.value,
                contents=[
                    self._text_compo(
                        text=data_type,
                        size=SIZE.SM.value,
                        **{
                            "gravity": "center",
                            "align": "center",
                            "flex": 1,
                        },
                    )
                ],
                **{"height": "30px"},
            ),
        ]

        for i in range(count):
            res.append(
                self._box_compo(
                    layout=LAYOUT.HORIZONTAL.value,
                    contents=[self._filler()],
                    **{
                        "backgroundColor": "#0367D3",
                        "height": "2px",
                    },
                )
            )
            if data_type == self.WEATHER_DATA:
                res.append(
                    self._box_compo(
                        layout=LAYOUT.HORIZONTAL.value,
                        contents=[
                            self._text_compo(
                                text=kwargs["wx"][i],
                                size=SIZE.XS.value,
                                **{
                                    "color": "#8c8c8c",
                                    "wrap": True,
                                    "gravity": "center",
                                    "align": "center",
                                },
                            )
                        ],
                        **{
                            "height": "70px",
                            "justifyContent": "center",
                        },
                    )
                )
            elif data_type == self.TEMPER_DATA:
                res.append(
                    self._box_compo(
                        layout=LAYOUT.HORIZONTAL.value,
                        contents=[
                            self._text_compo(
                                text=kwargs["temper"][i],
                                size=SIZE.SM.value,
                                **{
                                    "color": "#8c8c8c",
                                    "flex": 2,
                                    "align": "center",
                                    "gravity": "center",
                                    "wrap": True,
                                },
                            )
                        ],
                        **{
                            "height": "70px",
                        },
                    )
                )
            else:
                start_str = kwargs["time_start"][i].strftime("%m-%d %H:%M")
                end_str = (kwargs["time_start"][i] + timedelta(hours=12)).strftime(
                    "%m-%d %H:%M"
                )
                res.append(
                    self._box_compo(
                        layout=LAYOUT.HORIZONTAL.value,
                        contents=[
                            self._box_compo(
                                layout=LAYOUT.VERTICAL.value,
                                contents=[
                                    self._text_compo(
                                        text=start_str,
                                        size=SIZE.XXS.value,
                                        **{
                                            "color": "#8c8c8c",
                                            "flex": 2,
                                            "align": "center",
                                            "gravity": "center",
                                            "wrap": True,
                                        },
                                    ),
                                    self._text_compo(
                                        text=end_str,
                                        size=SIZE.XXS.value,
                                        **{
                                            "color": "#8c8c8c",
                                            "flex": 2,
                                            "align": "center",
                                            "gravity": "center",
                                            "wrap": True,
                                        },
                                    ),
                                ],
                            )
                        ],
                        **{
                            "height": "70px",
                        },
                    )
                )

        return self._box_compo(layout=LAYOUT.VERTICAL.value, contents=res)

    def _header(self, loc, *args, **kwargs):
        self.flex["header"] = self._box_compo(
            layout=LAYOUT.VERTICAL.value,
            contents=[
                self._text_compo(
                    text="天氣", size=SIZE.SM.value, **{"color": "#ffffff66"}
                ),
                self._text_compo(
                    text=loc,
                    size=SIZE.XL.value,
                    **{
                        "color": "#ffffff",
                        "weight": "bold",
                    },
                ),
            ],
            **{
                "paddingAll": "20px",
                "backgroundColor": "#0367D3",
                "paddingTop": "22px",
            },
        )

    def _body(self, time_start, temper, wx, desc):
        self.flex["body"] = self._box_compo(
            layout=LAYOUT.VERTICAL.value,
            contents=[
                self._box_compo(
                    layout=LAYOUT.VERTICAL.value,
                    contents=[
                        self._box_compo(
                            layout=LAYOUT.HORIZONTAL.value,
                            contents=[
                                self._text_compo(
                                    text="天氣概況",
                                    size=SIZE.SM.value,
                                    **{
                                        "gravity": "center",
                                    },
                                ),
                            ],
                            **{
                                "flex": 1,
                            },
                        ),
                        self._box_compo(
                            layout=LAYOUT.HORIZONTAL.value,
                            contents=[
                                self._box_compo(
                                    layout=LAYOUT.VERTICAL.value,
                                    contents=[self._filler()],
                                    **{
                                        "cornerRadius": "30px",
                                        "width": "12px",
                                        "height": "12px",
                                        "borderWidth": "2px",
                                        "borderColor": "#6486E3",
                                    },
                                ),
                                self._text_compo(
                                    text=desc,
                                    size=SIZE.SM.value,
                                    **{
                                        "color": "#8c8c8c",
                                        "flex": 2,
                                        "wrap": True,
                                    },
                                ),
                            ],
                            **{
                                "spacing": SIZE.MD.value,
                            },
                        ),
                    ],
                    **{
                        "spacing": SIZE.MD.value,
                    },
                ),
                self._box_compo(
                    layout=LAYOUT.HORIZONTAL.value,
                    contents=[
                        self._text_compo(text="今明24小時天氣預報預報", size=SIZE.SM.value)
                    ],
                    **{
                        "flex": 1,
                    },
                ),
                self._box_compo(
                    layout=LAYOUT.HORIZONTAL.value,
                    contents=[
                        self._make_data_box(
                            self.DATE_DATA, self.MAX_DATA, time_start=time_start
                        ),
                        self._make_data_box(
                            self.TEMPER_DATA, self.MAX_DATA, temper=temper
                        ),
                        self._make_data_box(self.WEATHER_DATA, self.MAX_DATA, wx=wx),
                    ],
                ),
            ],
            **{
                "spacing": "xl",
            },
        )

    def _footer(self, dt_main: list[str], w_pic: list[str], t: list[str], s: list[int]):
        self.flex["footer"] = self._box_compo(
            layout=LAYOUT.HORIZONTAL.value,
            contents=self._full_hour_content(dt_main, w_pic, t, s),
            **{"offsetEnd": "sm"},
        )

    def run(self, **kwargs) -> None:
        self._header(kwargs["loc"])
        self._body(kwargs["time_start"], kwargs["temper"], kwargs["wx"], kwargs["desc"])
        self._footer(kwargs["dt_main"], kwargs["w_pic"], kwargs["t"], kwargs["s"])


class FlexMessageMaker2(BaseFlexMessageMaker):
    def __init__(self, _type, size):
        super().__init__(_type, size)

    def _header(self, city):
        self.flex["header"] = self._box_compo(
            layout=LAYOUT.VERTICAL.value,
            contents=[
                self._box_compo(
                    layout=LAYOUT.VERTICAL.value,
                    contents=[
                        self._text_compo(
                            text=f"{city} 18小時內天氣預報",
                            size=SIZE.SM.value,
                            **{
                                "color": "#ffffff",
                            },
                        ),
                    ],
                ),
            ],
            **{
                "paddingAll": "20px",
                "spacing": SIZE.MD.value,
                "paddingTop": "22px",
                "backgroundColor": "#0367D3",
            },
        )

    def _body(self, dt_main: list[str], w_pic: list[str], t: list[str], s: list[int]):
        self.flex["body"] = self._box_compo(
            layout=LAYOUT.VERTICAL.value,
            contents=self._full_hour_content(dt_main, w_pic, t, s),
        )

    def run(
        self,
        city: str,
        dt_main: list[str],
        w_pic: list[str],
        t: list[str],
        s: list[int],
        has_header=True,
    ) -> None:
        if has_header:
            self._header(city)
        self._body(dt_main, w_pic, t, s)


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
