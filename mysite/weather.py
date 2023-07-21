import json
from datetime import datetime

import requests
from linebot.models import FlexSendMessage, TextSendMessage

from config import line_bot_api, OPENWEATHER_URL, cache, app, FROM_APP, TOKEN
from mysite.utils import WeatherDataParser


def today_weather(_from, *args, **kwargs):
    if _from == FROM_APP:
        event = kwargs["event"]
        text = event.message.text
    else:
        text = kwargs["text"]
        user_id = kwargs["user_id"]

    if "臺北" in text or "台北" in text:
        city = "台北市"
    elif "新北" in text:
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
    else:
        # Default city if none of the conditions match
        city = "台北市"

    cache_key = f"weather_F-C0032-001"
    data = cache.get(cache_key)
    if not data:
        url = f"{OPENWEATHER_URL}F-C0032-001?Authorization={TOKEN}&format=JSON"
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            cache.set(cache_key, data, 60 * 60)
            app.logger.warning(data)

        else:
            if _from == FROM_APP:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text="APIServerError: status={}".format(r.status_code)
                    ),
                )
            else:
                app.logger.error("APIServerError: status={}".format(r.status_code))

    issued = data["cwbopendata"]["dataset"]["datasetInfo"]["issueTime"]
    location = data["cwbopendata"]["dataset"]["location"]
    dict_city = {
        "台北市": 0,
        "新北市": 1,
        "基隆市": 6,
        "花蓮縣": 17,
        "宜蘭縣": 16,
        "金門縣": 20,
        "澎湖縣": 19,
        "台南市": 4,
        "高雄市": 5,
        "嘉義縣": 13,
        "嘉義市": 14,
        "苗栗縣": 9,
        "台中市": 3,
        "桃園市": 2,
        "新竹縣": 7,
        "新竹市": 8,
        "屏東縣": 15,
        "南投縣": 11,
        "臺東縣": 18,
        "彰化縣": 10,
        "雲林縣": 12,
        "連江縣": 21,
    }
    city_weather = location[dict_city.get(city, 0)]
    weather_elements = city_weather["weatherElement"]
    w_desc_time = weather_elements[0]["time"]
    MaxT = weather_elements[1]
    MinT = weather_elements[2]
    Time_start, Time_end = [], []
    wx = []
    for ele in w_desc_time:
        dt_start = datetime.strptime(ele["startTime"], "%Y-%m-%dT%H:%M:%S%z")
        Time_start.append(dt_start)

    maxT, minT = "", ""
    temper = []
    for i in range(len(w_desc_time) - 1):
        wx.append(w_desc_time[i]["parameter"]["parameterName"])
        maxT = MaxT["time"][i]["parameter"]["parameterName"]
        minT = MinT["time"][i]["parameter"]["parameterName"]
        temper.append(minT + "°C" + " ~ " + maxT + "°C")

    # 天氣小幫手
    dict_helper = {
        "台北市": "009",
        "新北市": "010",
        "基隆市": "011",
        "花蓮縣": "012",
        "宜蘭縣": "013",
        "金門縣": "014",
        "澎湖縣": "015",
        "台南市": "016",
        "高雄市": "017",
        "嘉義縣": "018",
        "嘉義市": "019",
        "苗栗縣": "020",
        "台中市": "021",
        "桃園市": "022",
        "新竹縣": "023",
        "新竹市": "024",
        "屏東縣": "025",
        "南投縣": "026",
        "臺東縣": "027",
        "彰化縣": "028",
        "雲林縣": "029",
        "連江縣": "030",
    }
    cache_key = f"helper_F-C0032-{dict_helper.get(city, '009')}"
    data = cache.get(cache_key)
    if not data:
        url = f"{OPENWEATHER_URL}F-C0032-{dict_helper.get(city, '009')}?Authorization={TOKEN}&format=JSON"
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            cache.set(cache_key, data, 60 * 60)
            app.logger.warning(data)
        else:
            if _from == FROM_APP:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text="APIServerError: status={}".format(r.status_code)
                    ),
                )
            else:
                app.logger.error("APIServerError: status={}".format(r.status_code))
    location = data["cwbopendata"]["dataset"]["location"]["locationName"]
    weather_helper = data["cwbopendata"]["dataset"]["parameterSet"]
    header = weather_helper["parameterSetName"]
    weather_elements = weather_helper["parameter"]
    comment = weather_elements[2]["parameterValue"]

    wdp = WeatherDataParser(
        location=location,
        date=Time_start,
        temper=temper,
        weather=wx,
        comment=comment,
        issued=issued,
    )
    flex_s = wdp.make_json()
    flex = json.loads(flex_s)

    alt_text = f"{city}天氣預報"
    if _from == FROM_APP:
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text=alt_text, contents=flex),
        )
    else:
        line_bot_api.push_message(
            user_id, FlexSendMessage(alt_text=alt_text, contents=flex)
        )
