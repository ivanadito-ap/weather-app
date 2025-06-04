from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/fetch-weather')
def fetch_weather():
    city = request.args.get('city')
    api_key = request.args.get('api_key')
    
    if not city or not api_key:
        return jsonify({"error": "City and API key are required"}), 400
    
    try:
        # Fetch current weather
        current_response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        )
        current_response.raise_for_status()
        current_data = current_response.json()
        
        # Fetch forecast
        forecast_response = requests.get(
            f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&cnt=5"
        )
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
        
        # Process current weather
        current_weather = {
            "city": current_data["name"],
            "temp": current_data["main"]["temp"],
            "humidity": current_data["main"]["humidity"],
            "conditions": current_data["weather"][0]["description"]
        }
        
        # Process forecast
        forecast = []
        for item in forecast_data["list"]:
            forecast.append({
                "date": item["dt_txt"],
                "temp": item["main"]["temp"],
                "conditions": item["weather"][0]["description"]
            })
        
        return jsonify({
            "current": current_weather,
            "forecast": forecast
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
