import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
weatherData = requests.get(
    'https://www.weather.go.kr/w/obs-climate/land/city-obs.do?auto_man=m&stn=0&dtm=&type=t99&reg=100&tm=', headers=headers)

weatherSoup = BeautifulSoup(weatherData.text, 'html.parser')
weatherData_rain = weatherSoup.select_one(
    '#weather_table > tbody > tr:nth-child(42) > td:nth-child(9)').text
weatherData_snow = weatherSoup.select_one(
    '#weather_table > tbody > tr:nth-child(42) > td:nth-child(10)').text

weatherData_rain_result = ""
weatherData_snow_result = ""
weatherPoints_rain = 0
weatherPoints_snow = 0

if (weatherData_rain.isspace() == True):
    weatherData_rain_result = "강수 확률이 없습니다."
    weatherPoints_rain = 40
else:
    weatherData_rain_result = weatherData_rain
    weatherPoints_rain = -30


if (weatherData_snow.isspace() == True):
    weatherData_snow_result = "강설 확률이 없습니다."
    weatherPoints_snow = 0
else:
    weatherData_snow_result = weatherData_snow
    weatherPoints_snow = 40

weatherData_list = [weatherData_rain_result, weatherData_snow_result]
weatherPoints_list = [weatherPoints_rain, weatherPoints_snow]

print(weatherPoints_snow, weatherPoints_rain)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/weather", methods=["GET"])
def weather_get():
    return jsonify({'weatherLists': weatherData_list, 'weatherpoints': weatherPoints_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
