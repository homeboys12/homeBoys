import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
weatherData = requests.get(
    'https://www.weather.go.kr/w/obs-climate/land/city-obs.do?auto_man=m&stn=0&dtm=&type=t99&reg=100&tm=', headers=headers)

weatherSoup = BeautifulSoup(weatherData.text, 'html.parser')

# 강수, 적설 크롤링
weatherData_rain = weatherSoup.select_one(
    '#weather_table > tbody > tr:nth-child(42) > td:nth-child(9)').text
weatherData_snow = weatherSoup.select_one(
    '#weather_table > tbody > tr:nth-child(42) > td:nth-child(10)').text

# 기상상태 메시지 입력을 위한 변수 생성
weatherData_rain_msg = ""
weatherData_snow_msg = ""

# 기상상태 점수 입력을 위한 변수 생성
weatherPoints_rain = 0
weatherPoints_snow = 0

# 현재 강수, 적설량 표현을 위한 변수 생성
weatherData_result_rain = 0
weatherData_result_snow = 0


# 현재 강수, 적설 상태 확인
if (weatherData_rain.isspace() == True):
    weatherData_rain_msg = "비 예보가없습니다."
    weatherPoints_rain = 40
    weatherData_rain = 0

elif (float(weatherData_rain) < float(3.0)):
    weatherData_rain_msg = "약한 비 예보가 있습니다."
    weatherPoints_rain = -30


elif (float(weatherData_rain) < float(15.0)):
    weatherData_rain_msg = "비 예보가 있습니다."
    weatherPoints_rain = -30


elif (float(14.0) < float(weatherData_rain)):
    weatherData_rain_msg = "강한 비 예보가 있습니다."
    weatherPoints_rain = -30


if (weatherData_snow.isspace() == True):
    weatherData_snow_msg = "눈 예보가 없습니다."
    weatherPoints_snow = 0
    weatherData_snow = 0
else:
    weatherData_snow_msg = "눈 예보가 있습니다."
    weatherData_snow_result = weatherData_snow
    weatherPoints_snow = 40

# 현재 강수, 적설 데이터를 가지는 리스트 생성
weatherMsg_list = [weatherData_rain_msg, weatherData_snow_msg]
weatherPoints_list = [weatherPoints_rain, weatherPoints_snow]
weatherResult_list = [float(weatherData_rain), float(weatherData_snow)]

# 잘 나오는 지 확인
print(weatherPoints_snow, weatherPoints_rain)
print(weatherData_rain_msg)
print(weatherResult_list)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/weather", methods=["GET"])
def weather_get():
    return jsonify({'weatherMsgLists': weatherMsg_list,
                    'weatherPoints': weatherPoints_list,
                    'weatherResult': weatherResult_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
