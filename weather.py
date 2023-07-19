from datetime import datetime
from zoneinfo import ZoneInfo

class weather_data():
    '''
        weather json data class
    '''
    def __init__(self, location, date, temper, weather, comment):
        self.location=location
        self.date=date
        self.temper=temper
        self.weather=weather
        self.comment=comment

    def make_weather_box(self):
        def make_weather():
            json = ''
            for i in range (len(self.weather)):
                tmp = '''
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "filler"
                  }
                ],
                "background_color": "#0367D3",
                "height": "2px"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "''' + self.weather[i] + '''",
                    "size": "xs",
                    "color": "#8c8c8c",
                    "flex": 2,
                    "gravity": "center",
                    "wrap": true,
                    "offset_start": "5px"
                  }
                ],
                "height": "70px"
              }'''
                json += tmp
                if i != len(self.weather)-1: json += ','
            return json 

        json = '''
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
                    "text": "天氣",
                    "gravity": "center",
                    "size": "sm",
                    "align": "center",
                    "flex": 1
                  }
                ],
                "height": "30px"
              },''' + make_weather() + '''
            ]
          }'''
        return json 


    def make_dates_box(self):
        def make_date():
            json = ''
            for i in range (len(self.date)):
                if i == len(self.date)-1: break 
                tmp = '''
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "filler"
                  }
                ],
                "background_color": "#0367D3",
                "height": "2px"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "''' + self.date[i] + '''",
                    "size": "sm",
                    "color": "#8c8c8c",
                    "flex": 2,
                    "align": "center",
                    "gravity": "center",
                    "wrap": true
                  }
                ],
                "height": "70px"
              }'''
                json += tmp
                if i != len(self.date)-2: json += ','
            return json

        json = '''
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
                    "text": "時間",
                    "gravity": "center",
                    "size": "sm",
                    "align": "center",
                    "flex": 1
                  }
                ],
                "height": "30px"
              },''' + make_date() + '''
            ]
          },'''
        return json

    def make_temper_box(self):
        def make_temper():
            json = ''
            for i in range (len(self.temper)):
                tmp = '''
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "filler"
                  }
                ],
                "background_color": "#0367D3",
                "height": "2px"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "''' + self.temper[i] + '''",
                    "size": "xs",
                    "color": "#8c8c8c",
                    "flex": 2,
                    "align": "center",
                    "gravity": "center",
                    "wrap": true
                  }
                ],
                "height": "70px"
              }'''
                json += tmp 
                if i != len(self.temper)-1: json += ','
            return json
        json = '''
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
                    "text": "氣溫",
                    "gravity": "center",
                    "size": "sm",
                    "align": "center",
                    "flex": 1
                  }
                ],
                "height": "30px"
              },''' + make_temper() + '''
            ]
          },'''
        return json

    def make_comment_box(self):
        json = '''
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  }
                ],
                "corner_radius": "30px",
                "width": "12px",
                "height": "12px",
                "border_width": "2px",
                "border_color": "#6486E3"
              },
              {
                "type": "text",
                "text": "''' + self.comment + '''",
                "size": "sm",
                "color": "#8c8c8c",
                "flex": 2,
                "wrap": true
              }
            ],
            "spacing": "md"
          }'''
        return json

    def make_json(self):
        json_data = '''{
  "type": "bubble",
  "size": "giga",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "天氣",
        "color": "#ffffff66",
        "size": "sm"
      },
      {
        "type": "text",
        "text": "''' + self.location + '''",
        "color": "#ffffff",
        "size": "xl",
        "weight": "bold"
      }
    ],
    "padding_all": "20px",
    "background_color": "#0367D3",
    "padding_top": "22px"
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
                "size": "sm"
              }
            ],
            "flex": 1
          },''' + self.make_comment_box() + '''
        ],
        "spacing": "md"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "text",
            "text": "今明24小時天氣預報預報",
            "size": "sm"
          }
        ],
        "flex": 1
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [''' + self.make_dates_box() + self.make_temper_box() + self.make_weather_box() +'''
        ]
      },
      {
        "type": "text",
        "text": "Update: ''' + datetime.now().replace(tzinfo=ZoneInfo('Asia/Taipei')).strftime('%Y/%m/%d %H:%M') + '''",
        "color": "#b7b7b7",
        "size": "xs",
        "align": "end"
      }
    ],
    "spacing": "xl"
  }
}'''
        return json_data 
