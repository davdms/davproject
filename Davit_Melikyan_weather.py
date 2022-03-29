from flask import Flask
import requests

app = Flask(__name__)

@app.route("/weather/<lat>/<lon>")
def weather_lon_lat(lat, lon):
    response = requests.get(f"https://www.7timer.info/bin/astro.php?lon={lon}&lat={lat}&ac=0&unit=metric&output=json&tzshift=0")

    if response.status_code == 200:
        data = response.json()
        dataseries = data.get('dataseries')
        sum_of_temperature = 0

        for val in dataseries:
            sum_of_temperature += val.get('temp2m')
        return str(sum_of_temperature / len(dataseries))

    return None

@app.route("/weather")
def weather():
    response = "<p>Weather</p>"
    return response

if __name__ == "__main__":
    app.run()