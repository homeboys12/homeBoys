import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/temperature', methods=['GET'])
def test_get():
   headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

   data = requests.get(
      'https://search.naver.com/search.naver?sm=tab_sug.top&where=nexearch&query=%EC%84%9C%EC%9A%B8+%EC%97%AC%EC%9D%98%EB%8F%84+%EB%82%A0%EC%94%A8&oquery=%EB%82%A0%EC%94%A8&tqi=hG3eTwp0Jy0ssKeqm0wssssstIV-100184&acq=%EC%84%9C%EC%9A%B8+%EC%97%AC%EC%9D%98%EB%8F%84+%EB%82%A0%EC%94%A8&acr=1&qdt=0',
      headers=headers)
   soup = BeautifulSoup(data.text, 'html.parser')

   arr = []

   title = soup.select_one(
      '#main_pack > section.sc_new.cs_weather_new._cs_weather > div._tab_flicking > div.content_wrap > div.open > div:nth-child(1) > div > div.weather_info > div > div._today > div.weather_graphic > div.temperature_text > strong')

   for title2 in title:
      arr.append(title2.text)

   temperature = float(arr[1])
   if float(arr[1]) <= 5:
      score = -30
      text = "오늘은 날씨가 매우 춥네요"
   elif 5 < float(arr[1]) <= 10:
      score = -20
      text = "오늘은 날씨가 춥네요"
   elif 10 < float(arr[1]) <= 15:
      score = 0
      text = "오늘은 좀 쌀쌀 할 수 있어요"
   elif 15 < float(arr[1]) <= 20:
      score = 20
      text = "오늘은 밖에 나가시기 좋은 날씨 입니다"
   elif 20 < float(arr[1]) <= 27:
      score = 30
      text = "오늘은 밖에 나가기 완벽한 날씨입니다."
   else:
      score = -30
      text = "오늘은 매우 더울것으로 예상됩니다"
   print(temperature)
   return jsonify({'temperature': temperature, 'score': score, 'text': text})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)