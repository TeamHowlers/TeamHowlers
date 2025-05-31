from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    cities = ['London', 'Paris', 'New York']
    weather_data = []
    for city in cities:
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=<Your API Key>')
        data = response.json()
        weather_data.append({
            'city': city,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure']
        })
    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True)