import requests

def get_weather(city):
    api_key = "b9b9383dd74979c04706a26a7cd18bc4"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    data = requests.get(url).json()

    print(data)  # 👈 ADD THIS LINE

    if "main" not in data:
        return {
            "temp": "Error",
            "humidity": "Error",
            "condition": data.get("message", "API issue")
        }

    return {
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"]
    }