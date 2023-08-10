from linebot.v3.messaging import ApiClient, MessagingApi

from config import FROM_TASK, USER1, USER2, configuration
from mysite.weather import get_today_weather


def job():
    """
    original function is setting a scheduler on heroku server
    line bot would auto push weather forcast at 7:00 A.M. every morning
    weather forcast flex message made from weather.py
    weather data come from https://opendata.cwb.gov.tw/index
    """
    send_list = [
        {
            "city": "台北",
            "user": USER2,
        },
        {
            "city": "新北",
            "user": USER1,
        },
    ]
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        for data in send_list:
            get_today_weather(
                FROM_TASK, line_bot_api, text=data["city"], user_id=data["user"]
            )


if __name__ == "__main__":
    job()
