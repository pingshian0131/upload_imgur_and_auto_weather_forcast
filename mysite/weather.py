import json
from datetime import datetime

import requests
from linebot.models import FlexSendMessage, TextSendMessage
from linebot.v3.messaging import (
    ReplyMessageRequest,
    TextMessage,
    FlexMessage,
    PushMessageRequest,
    FlexContainer,
)

from config import OPENWEATHER_URL, cache, app, FROM_APP
from config import OPENWEATHER_TOKEN as TOKEN
from mysite.utils import WeatherDataParser


def today_weather(_from, line_bot_api, *args, **kwargs):
    print("aaa")
    if _from == FROM_APP:
        event = kwargs["event"]
        text = event.message.text
    else:
        event = None
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
    # data = {
    #     "cwbopendata": {
    #         "@xmlns": "urn:cwb:gov:tw:cwbcommon:0.1",
    #         "identifier": "3c69e5b0-44db-fdad-e66d-e2069b624190",
    #         "sender": "weather@cwb.gov.tw",
    #         "sent": "2023-08-10T07:18:02+08:00",
    #         "status": "Actual",
    #         "msgType": "Issue",
    #         "source": "MFC",
    #         "dataid": "C0032-001",
    #         "scope": "Public",
    #         "dataset": {
    #             "datasetInfo": {
    #                 "datasetDescription": "三十六小時天氣預報",
    #                 "issueTime": "2023-08-10T05:00:00+08:00",
    #                 "update": "2023-08-10T07:18:02+08:00",
    #             },
    #             "location": [
    #                 {
    #                     "locationName": "臺北市",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰短暫陣雨或雷雨",
    #                                         "parameterValue": "18",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰時多雲",
    #                                         "parameterValue": "6",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲時陰短暫陣雨或雷雨",
    #                                         "parameterValue": "16",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "35",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "31",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "32",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "28",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "27",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "27",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "悶熱至易中暑"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "80",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "80",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "新北市",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰時多雲短暫陣雨或雷雨",
    #                                         "parameterValue": "17",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲",
    #                                         "parameterValue": "4",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲時陰短暫陣雨或雷雨",
    #                                         "parameterValue": "16",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "34",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "31",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "32",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "28",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "27",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "27",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "悶熱至易中暑"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "70",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "80",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "桃園市",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲時陰短暫陣雨或雷雨",
    #                                         "parameterValue": "16",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲",
    #                                         "parameterValue": "4",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰時多雲短暫陣雨或雷雨",
    #                                         "parameterValue": "17",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "33",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "32",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "28",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "70",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "80",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "臺中市",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲短暫陣雨或雷雨",
    #                                         "parameterValue": "15",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲時陰",
    #                                         "parameterValue": "5",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰短暫陣雨或雷雨",
    #                                         "parameterValue": "18",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "32",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "32",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "28",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "27",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "27",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "70",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "70",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "臺南市",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰短暫陣雨或雷雨",
    #                                         "parameterValue": "18",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰短暫陣雨或雷雨",
    #                                         "parameterValue": "18",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰時多雲短暫陣雨或雷雨",
    #                                         "parameterValue": "17",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "29",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "28",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "27",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "27",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "60",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "50",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "50",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "高雄市",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰短暫陣雨或雷雨",
    #                                         "parameterValue": "18",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰短暫陣雨或雷雨",
    #                                         "parameterValue": "18",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰短暫陣雨或雷雨",
    #                                         "parameterValue": "18",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "29",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "28",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "27",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "27",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "70",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "60",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "60",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "基隆市",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲午後短暫雷陣雨",
    #                                         "parameterValue": "22",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲",
    #                                         "parameterValue": "4",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲午後短暫雷陣雨",
    #                                         "parameterValue": "22",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "33",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "31",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "28",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "27",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "27",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "悶熱至易中暑"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "60",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "50",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "新竹縣",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰時多雲短暫陣雨或雷雨",
    #                                         "parameterValue": "17",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲時陰",
    #                                         "parameterValue": "5",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰短暫陣雨或雷雨",
    #                                         "parameterValue": "18",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "33",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "32",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "28",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "50",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "新竹市",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰時多雲短暫陣雨或雷雨",
    #                                         "parameterValue": "17",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲時陰",
    #                                         "parameterValue": "5",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰天",
    #                                         "parameterValue": "7",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "32",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "31",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "28",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "40",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "苗栗縣",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲短暫陣雨或雷雨",
    #                                         "parameterValue": "15",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲時陰",
    #                                         "parameterValue": "5",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰時多雲",
    #                                         "parameterValue": "6",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "32",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "31",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "28",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "60",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "彰化縣",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲短暫陣雨或雷雨",
    #                                         "parameterValue": "15",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲時陰",
    #                                         "parameterValue": "5",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰短暫陣雨或雷雨",
    #                                         "parameterValue": "18",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "32",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "31",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "27",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "60",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "60",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "南投縣",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲時陰",
    #                                         "parameterValue": "5",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰時多雲",
    #                                         "parameterValue": "6",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰天",
    #                                         "parameterValue": "7",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "32",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "29",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "31",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "雲林縣",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲時陰",
    #                                         "parameterValue": "5",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰時多雲",
    #                                         "parameterValue": "6",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰短暫陣雨或雷雨",
    #                                         "parameterValue": "18",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "31",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "28",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "31",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "50",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "嘉義縣",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰時多雲短暫陣雨或雷雨",
    #                                         "parameterValue": "17",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰天",
    #                                         "parameterValue": "7",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰短暫陣雨或雷雨",
    #                                         "parameterValue": "18",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "31",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "29",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "31",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "60",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "70",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "嘉義市",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲時陰短暫陣雨或雷雨",
    #                                         "parameterValue": "16",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰時多雲",
    #                                         "parameterValue": "6",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰短暫陣雨或雷雨",
    #                                         "parameterValue": "18",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "31",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "28",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "31",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "60",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "50",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "屏東縣",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰短暫陣雨或雷雨",
    #                                         "parameterValue": "18",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰短暫陣雨或雷雨",
    #                                         "parameterValue": "18",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰短暫陣雨或雷雨",
    #                                         "parameterValue": "18",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "28",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "90",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "50",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "80",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "宜蘭縣",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰時多雲",
    #                                         "parameterValue": "6",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰時多雲",
    #                                         "parameterValue": "6",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲午後短暫雷陣雨",
    #                                         "parameterValue": "22",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "33",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "32",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "27",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至易中暑"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "40",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "花蓮縣",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲時晴",
    #                                         "parameterValue": "3",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰時多雲",
    #                                         "parameterValue": "6",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲午後短暫雷陣雨",
    #                                         "parameterValue": "22",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "33",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "臺東縣",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲時陰",
    #                                         "parameterValue": "5",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲",
    #                                         "parameterValue": "4",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲時陰",
    #                                         "parameterValue": "5",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "32",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "27",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至易中暑"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "澎湖縣",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰短暫陣雨或雷雨",
    #                                         "parameterValue": "18",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰時多雲短暫陣雨或雷雨",
    #                                         "parameterValue": "17",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰短暫陣雨或雷雨",
    #                                         "parameterValue": "18",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "28",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "28",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "27",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "27",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "40",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "40",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "金門縣",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰時多雲短暫陣雨或雷雨",
    #                                         "parameterValue": "17",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰時多雲短暫陣雨或雷雨",
    #                                         "parameterValue": "17",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲時陰",
    #                                         "parameterValue": "5",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "32",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "28",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "27",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "locationName": "連江縣",
    #                     "weatherElement": [
    #                         {
    #                             "elementName": "Wx",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰時多雲",
    #                                         "parameterValue": "6",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "多雲短暫陣雨或雷雨",
    #                                         "parameterValue": "15",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "陰時多雲短暫陣雨或雷雨",
    #                                         "parameterValue": "17",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MaxT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "29",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "27",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "29",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "MinT",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "27",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "26",
    #                                         "parameterUnit": "C",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "CI",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適"},
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {"parameterName": "舒適至悶熱"},
    #                                 },
    #                             ],
    #                         },
    #                         {
    #                             "elementName": "PoP",
    #                             "time": [
    #                                 {
    #                                     "startTime": "2023-08-10T06:00:00+08:00",
    #                                     "endTime": "2023-08-10T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "20",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-10T18:00:00+08:00",
    #                                     "endTime": "2023-08-11T06:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                                 {
    #                                     "startTime": "2023-08-11T06:00:00+08:00",
    #                                     "endTime": "2023-08-11T18:00:00+08:00",
    #                                     "parameter": {
    #                                         "parameterName": "30",
    #                                         "parameterUnit": "百分比",
    #                                     },
    #                                 },
    #                             ],
    #                         },
    #                     ],
    #                 },
    #             ],
    #         },
    #     }
    # }

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
    # data = {
    #     "cwbopendata": {
    #         "@xmlns": "urn:cwb:gov:tw:cwbcommon:0.1",
    #         "identifier": "3a481e21-16a9-9d31-3f4f-e2a80c404c0c",
    #         "sender": "weather@cwb.gov.tw",
    #         "sent": "2023-08-10T06:50:16+08:00",
    #         "status": "Actual",
    #         "msgType": "Issue",
    #         "scope": "Public",
    #         "dataid": "F-C0032-010",
    #         "source": "Weather Forecast Center",
    #         "dataset": {
    #             "datasetInfo": {
    #                 "datasetDescription": "WeatherAssistant",
    #                 "datasetLanguage": "zh-TW",
    #                 "issueTime": "2023-08-10T06:49:10+08:00",
    #             },
    #             "location": {
    #                 "locationName": "新北市",
    #                 "stationId": "46692",
    #                 "geocode": "65",
    #             },
    #             "parameterSet": {
    #                 "parameterSetName": "天氣小幫手描述",
    #                 "parameter": [
    #                     {"parameterValue": "多雲短暫陣雨或雷雨，出門請攜帶雨具備用，外出做好防曬以免中暑。"},
    #                     {"parameterValue": "昨天（９日）天氣穩定，雲量較多但仍有陽光，新北站高溫36.4度。"},
    #                     {
    #                         "parameterValue": "今天（１０日）西南風影響且水氣增加，天氣多雲短暫陣雨或雷雨，出門請攜帶雨具備用，氣溫27-33度，外出活動請做好防曬並補充水分以免中暑。"
    #                     },
    #                     {"parameterValue": "北海岸沿海有長浪發生的機率，請注意。"},
    #                 ],
    #             },
    #         },
    #     }
    # }
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
    flex = wdp.make_json()

    alt_text = f"{city}天氣預報"
    if _from == FROM_APP:
        print("FROM_APP")
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
            user_id, messages=[FlexMessage(alt_text=alt_text, contents=flex)]
        )
