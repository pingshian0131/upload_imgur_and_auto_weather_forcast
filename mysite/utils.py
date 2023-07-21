from datetime import datetime, timedelta


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
        def make_weather():
            json_str = ""
            for i in range(len(self.weather)):
                tmp = (
                    '''
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
                    "text": "'''
                    + self.weather[i]
                    + '''",
                    "size": "sm",
                    "color": "#8c8c8c",
                    "wrap": true,
                    "gravity": "center",
                    "align": "center"
                  }
                ],
                "height": "70px",
                "justify_content": "center"
              }'''
                )
                json_str += tmp
                if i != len(self.weather) - 1:
                    json_str += ","
            return json_str

        return (
            """
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
              },"""
            + make_weather()
            + """
            ]
          }"""
        )

    def _make_dates_box(self):
        def make_date():
            json_str = ""
            for i in range(len(self.date) - 1):
                tmp = (
                    '''
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
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": "'''
                    + self.date[i].strftime("%m-%d %H:%M")
                    + '''",
                        "size": "sm",
                        "color": "#8c8c8c",
                        "flex": 2,
                        "align": "center",
                        "gravity": "center",
                        "wrap": true
                      },
                      {
                        "type": "text",
                        "text": "'''
                    + (self.date[i] + timedelta(hours=12)).strftime("%m-%d %H:%M")
                    + '''",
                        "size": "sm",
                        "color": "#8c8c8c",
                        "flex": 2,
                        "align": "center",
                        "gravity": "center",
                        "wrap": true
                      }
                    ]
                  }
                ],
                "height": "70px"
              }'''
                )
                json_str += tmp
                if i != len(self.date) - 2:
                    json_str += ","
            return json_str

        return (
            """
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
              },"""
            + make_date()
            + """
            ]
          },"""
        )

    def _make_temper_box(self):
        def make_temper():
            json_str = ""
            for i in range(len(self.temper)):
                tmp = (
                    '''
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
                    "text": "'''
                    + self.temper[i]
                    + """",
                    "size": "md",
                    "color": "#8c8c8c",
                    "flex": 2,
                    "align": "center",
                    "gravity": "center",
                    "wrap": true
                  }
                ],
                "height": "70px"
              }"""
                )
                json_str += tmp
                if i != len(self.temper) - 1:
                    json_str += ","
            return json_str

        return (
            """
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
              },"""
            + make_temper()
            + """
            ]
          },"""
        )

    def _make_comment_box(self):
        json = (
            '''
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
                "text": "'''
            + self.comment
            + """",
                "size": "sm",
                "color": "#8c8c8c",
                "flex": 2,
                "wrap": true
              }
            ],
            "spacing": "md"
          }"""
        )
        return json

    def make_json(self):
        return (
            '''{
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
        "text": "'''
            + self.location
            + """",
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
          },"""
            + self._make_comment_box()
            + """
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
        "contents": ["""
            + self._make_dates_box()
            + self._make_temper_box()
            + self._make_weather_box()
            + """
        ]
      },
      {
        "type": "text",
        "text": "最後更新時間: """
            + datetime.strptime(self.issued, "%Y-%m-%dT%H:%M:%S%z").strftime(
                "%Y-%m-%d %H:%M"
            )
            + """",
        "color": "#b7b7b7",
        "size": "xs",
        "align": "end"
      }
    ],
    "spacing": "xl"
  }
}"""
        )
