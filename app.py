import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

# weatherpart@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
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

# temperaturePart@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
temperatureData = requests.get(
    'https://search.naver.com/search.naver?sm=tab_sug.top&where=nexearch&query=%EC%84%9C%EC%9A%B8+%EC%97%AC%EC%9D%98%EB%8F%84+%EB%82%A0%EC%94%A8&oquery=%EB%82%A0%EC%94%A8&tqi=hG3eTwp0Jy0ssKeqm0wssssstIV-100184&acq=%EC%84%9C%EC%9A%B8+%EC%97%AC%EC%9D%98%EB%8F%84+%EB%82%A0%EC%94%A8&acr=1&qdt=0',
    headers=headers)
temperatureSoup = BeautifulSoup(temperatureData.text, 'html.parser')

temperature_arr = []

temperature_titles = temperatureSoup.select_one(
    '#main_pack > section.sc_new.cs_weather_new._cs_weather > div._tab_flicking > div.content_wrap > div.open > div:nth-child(1) > div > div.weather_info > div > div._today > div.weather_graphic > div.temperature_text > strong')

for temperature_title in temperature_titles:
    temperature_arr.append(temperature_title.text)

temperature = float(temperature_arr[1])
if float(temperature_arr[1]) <= 5:
    score = -30
    text = "오늘은 날씨가 매우 춥네요"
elif 5 < float(temperature_arr[1]) <= 10:
    score = -20
    text = "오늘은 날씨가 춥네요"
elif 10 < float(temperature_arr[1]) <= 15:
    score = 0
    text = "오늘은 좀 쌀쌀 할 수 있어요"
elif 15 < float(temperature_arr[1]) <= 20:
    score = 20
    text = "오늘은 밖에 나가시기 좋은 날씨 입니다"
elif 20 < float(temperature_arr[1]) <= 27:
    score = 30
    text = "오늘은 밖에 나가기 완벽한 날씨입니다."
else:
    score = -30
    text = "오늘은 매우 더울것으로 예상됩니다"

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
                    'weatherResult': weatherResult_list,
                    'temperature': temperature,
                    'temperature_score': score,
                    'temperature_text': text})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)


app = Flask(__name__)


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
uvData = requests.get('https://weather.naver.com/', headers=headers)

uvSoup = BeautifulSoup(uvData.text, 'html.parser')


uvStatus = uvSoup.select_one(
    '#lifeIndex > div.inner_card > div > div > ul > li:nth-child(1) > div').text.strip()
uvScore = 0

if (uvStatus == "낮음"):
    uvScore = 15
elif (uvStatus == "보통"):
    uvScore = 10
elif (uvStatus == "높음"):
    uvScore = 5
elif (uvStatus == "매우높음"):
    uvScore = 0
elif (uvStatus == "위험"):
    uvScore = -20
else:
    uvScore = '표시 내용이 없습니다'

uv_list = [uvStatus, uvScore]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/uv', methods=['GET'])
def uv_get():
    return jsonify({'uv': uv_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
