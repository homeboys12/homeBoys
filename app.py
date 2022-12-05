import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
weatherData = requests.get(
    'https://www.weather.go.kr/w/obs-climate/land/city-obs.do?auto_man=m&stn=0&dtm=&type=t99&reg=100&tm=', headers=headers)

weatherSoup = BeautifulSoup(weatherData.text, 'html.parser')
weatherData_rain = weatherSoup.select_one(
    '#weather_table > tbody > tr:nth-child(42) > td:nth-child(9)').text
weatherData_snow = weatherSoup.select_one(
    '#weather_table > tbody > tr:nth-child(42) > td:nth-child(10)')

print(weatherData_rain)

for weatherList in weatherLists:
    weatherList_result = weatherList.replace(" ", "강수예보가 없습니다.")
    print(weatherList_result)


# @app.route("/article", methods=["GET"])
# def article_get():

#     return jsonify({'lists': allArticleList})
