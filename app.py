import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

data = requests.get(
    'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%82%A0%EC%94%A8&oquery=%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80&tqi=hGIDolprvTVssPNfROCssssssG4-287014',
    headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

mise = soup.select_one('#main_pack > section.sc_new.cs_weather_new._cs_weather > div._tab_flicking > div.content_wrap > div.open > div:nth-child(1) > div > div.weather_info > div > div.report_card_wrap > ul > li:nth-child(1) > a > span')

mise_msg = ""
mise_score = 0

if mise.text == "매우좋음":
    mise_msg = "오늘 미세먼지가 매우좋습니다. 마스크 걱정없이 맑은공기 맡으러 외출해도 좋겠어요!"
    mise_score = 15
elif mise.text == "좋음":
    mise_msg = "오늘은 미세먼지가 좋네요 마스크 없이 외출해도 괜찮겠어요!"
    mise_score = 10
elif mise.text == "보통":
    mise_msg = "오늘은 미세먼지가 보통입니다. 마스크 쓰는걸 추천드립니다."
    mise_score = 0
elif mise.text == "나쁨":
    mise_msg = "오늘은 미세먼지가 안좋네요 마스크를 웬만하면 쓰는걸 추천드립니다. 호흡기 조심하세요!"
    mise_score = -10
elif mise.text == "매우나쁨":
    mise_msg = "오늘은 미세먼지가 매우나쁨입니다. 마스크는 꼭 써주세요!"
    mise_score = -15

mise_arr = [mise.text, mise_msg, mise_score]

# 데이터확인
print(mise_arr)

@app.route('/')
def home():
   return render_template('index.html')


@app.route('/mise', methods=['GET'])
def mise_get():
    return jsonify({'mise_list': mise_arr})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)