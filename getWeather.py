#!/usr/bin/python
# encoding:utf-8

import urllib
import pprint
import json
import sys
import os
import getWeather_CONSTANTS

APP_ID = getWeather_CONSTANTS.APP_ID

BASE_URL = "https://map.yahooapis.jp/weather/V1/"
COORDINATES = getWeather_CONSTANTS.COORDINATES
OUTPUT = "json"

url = BASE_URL + "place?coordinates=%s&appid=%s&output=%s" % (COORDINATES,APP_ID,OUTPUT)

json_tree = json.loads(urllib.urlopen(url).read())
# pprint.pprint(json_tree)

rain_level = 0
forecast_count = 0

for var in range(0,7):
    date = json_tree['Feature'][0]['Property']['WeatherList']['Weather'][var]['Date']
    rainfall = json_tree['Feature'][0]['Property']['WeatherList']['Weather'][var]['Rainfall']
    type = json_tree['Feature'][0]['Property']['WeatherList']['Weather'][var]['Type']
    #print("%s,%s,%s"%(date,rainfall,type))
    talk = ""

    if type == "observation":
        time = "今、雨"
        if rainfall == 0.0:
            suffix = "はふっていません。"
            talk = time + suffix
        
        else :
            suffix = "がふっています。"
            talk = time + suffix

    else :
        forecast_count = forecast_count + 1
        if rainfall > 5.0:
            rain_level = rain_level + 1

    if forecast_count == 6:
        
        time = "1時間以内に雨"
        end = "天気予報は以上です。"

        if rain_level >= 1:

            suffix = "がふりそうです。"

        else :
            suffix = "はふらないでしょう。"

        talk = time + suffix + end

    print talk
    
    if len(talk) > 0:
        os.system('/home/pi/Documents/aquestalkpi/AquesTalkPi -g 40 -s 80 "' + talk + '" | aplay')

