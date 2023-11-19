#!/usr/bin/env python

import json
import requests
from datetime import datetime

WEATHER_CODES = {
    '113': 'sunny',
    '116': 'partly_cloudy',
    '119': 'cloudy',
    '122': 'cloudy',
    '143': 'cloudy',
    '176': 'rainy',
    '179': 'rainy',
    '182': 'rainy',
    '185': 'rainy',
    '200': 'thundershower',
    '227': 'snowy',
    '230': 'snowy',
    '248': 'cloudy',
    '260': 'cloudy',
    '263': 'rainy',
    '266': 'rainy',
    '281': 'rainy',
    '284': 'rainy',
    '293': 'rainy',
    '296': 'rainy',
    '299': 'rainy',
    '302': 'rainy',
    '305': 'rainy',
    '308': 'rainy',
    '311': 'rainy',
    '314': 'rainy',
    '317': 'rainy',
    '320': 'snowy',
    '323': 'snowy',
    '326': 'snowy',
    '329': 'snowstorm',
    '332': 'snowstorm',
    '335': 'snowstorm',
    '338': 'snowstorm',
    '350': 'rainy',
    '353': 'rainy',
    '356': 'rainy',
    '359': 'rainy',
    '362': 'rainy',
    '365': 'rainy',
    '368': 'rainy',
    '371': 'snowstorm',
    '374': 'snowy',
    '377': 'snowy',
    '386': 'snowy',
    '389': 'snowy',
    '392': 'rainy',
    '395': 'snowstorm '
}

data = {}


weather = requests.get("https://wttr.in/?format=j1").json()


def format_time(time):
    return time.replace("00", "").zfill(2)


def format_temp(temp):
    return (hour['FeelsLikeC']+"°").ljust(3)


def format_chances(hour):
    chances = {
        "chanceoffog": "Fog",
        "chanceoffrost": "Frost",
        "chanceofovercast": "Overcast",
        "chanceofrain": "Rain",
        "chanceofsnow": "Snow",
        "chanceofsunshine": "Sunshine",
        "chanceofthunder": "Thunder",
        "chanceofwindy": "Wind"
    }

    conditions = []
    for event in chances.keys():
        if int(hour[event]) > 0:
            conditions.append(chances[event]+" "+hour[event]+"%")
    return ", ".join(conditions)

tempint = int(weather['current_condition'][0]['FeelsLikeC'])
extrachar = ''
if tempint > 0 and tempint < 10:
    extrachar = '+'

data['alt'] = WEATHER_CODES[weather['current_condition'][0]['weatherCode']]
data['text'] = extrachar+weather['current_condition'][0]['FeelsLikeC']+"°"

data['tooltip'] = f"<b>{weather['current_condition'][0]['weatherDesc'][0]['value']} {weather['current_condition'][0]['temp_C']}°</b>\n"
data['tooltip'] += f"Feels like: {weather['current_condition'][0]['FeelsLikeC']}°\n"
data['tooltip'] += f"Wind: {weather['current_condition'][0]['windspeedKmph']}Km/h\n"
data['tooltip'] += f"Humidity: {weather['current_condition'][0]['humidity']}%\n"
for i, day in enumerate(weather['weather']):
    data['tooltip'] += f"\n<b>"
    if i == 0:
        data['tooltip'] += "Today, "
    if i == 1:
        data['tooltip'] += "Tomorrow, "
    data['tooltip'] += f"{day['date']}</b>\n"
    data['tooltip'] += f"⬆️ {day['maxtempC']}° ⬇️ {day['mintempC']}° "
    data['tooltip'] += f"🌅 {day['astronomy'][0]['sunrise']} 🌇 {day['astronomy'][0]['sunset']}\n"
    for hour in day['hourly']:
        if i == 0:
            if int(format_time(hour['time'])) < datetime.now().hour-2:
                continue
        data['tooltip'] += f"{format_time(hour['time'])} {WEATHER_CODES[hour['weatherCode']]} {format_temp(hour['FeelsLikeC'])} {hour['weatherDesc'][0]['value']}, {format_chances(hour)}\n"


print(json.dumps(data))
