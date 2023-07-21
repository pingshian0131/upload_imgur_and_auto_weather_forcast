from config import FROM_TASK, USER_ID
from mysite.weather import today_weather


def job():
    """
    original function is setting a scheduler on heroku server
    line bot would auto push weather forcast at 7:00 A.M. every morning
    weather forcast flex message made from weather.py
    weather data come from https://opendata.cwb.gov.tw/index
    """
    today_weather(FROM_TASK, text="台北", user_id=USER_ID)


if __name__ == "__main__":
    job()
