from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "c68dbe744edf70ea53017e71f27b1802"


@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if city:
            try:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city},PK&appid={API_KEY}&units=metric"

                response = requests.get(url, timeout=5)
                data = response.json()

                if response.status_code == 200:
                    weather_data = {
                        "city": data["name"],
                        "temperature": data["main"]["temp"],
                        "description": data["weather"][0]["description"].capitalize(),
                        "humidity": data["main"]["humidity"],
                        "wind": data["wind"]["speed"]
                    }
                else:
                    weather_data = {
                        "error": "City not found. Please check spelling!"
                    }

            except requests.exceptions.RequestException:
                weather_data = {
                    "error": "Network error. Please try again!"
                }

    return render_template("index.html", weather=weather_data)


if __name__ == "__main__":
    app.run(debug=True)