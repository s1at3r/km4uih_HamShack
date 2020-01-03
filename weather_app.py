""" Weather app for portfolio """

"""Library Dependancies"""

from flask import Flask, render_template, request
import json
import requests
import pytemperature

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def weather():
    """ This function will retrive weather data from openweathermap."""
    if request.method == "POST":
        city = request.form["city"]
    else:
        city = "nashville"

    api = "d450efe05541dcf4285ee570f64f3b15"

    list_of_data = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + api
    ).json()

    data = {
        "country_code": str(list_of_data["sys"]["country"]),
        "name": list_of_data["name"],
        "lat": list_of_data["coord"]["lat"],
        "lon": list_of_data["coord"]["lon"],
        "temp_k": list_of_data["main"]["temp"],
        "temp_f": pytemperature.k2f(list_of_data["main"]["temp"]),
        "temp_c": pytemperature.k2c(list_of_data["main"]["temp"]),
        "pressure": str(list_of_data["main"]["pressure"]),
        "humidity": str(list_of_data["main"]["humidity"]),
    }

    print(data)
    return render_template("index.html", data=data)


@app.route("/callsign", methods=["POST", "GET"])
def callsign_lookup():
    """This function will allow allow for the lookup of amatuer radio callsign information"""
    if request.method == "POST":
        callsign = request.form["callsign"]
        callsign_data = requests.get(
            "https://callook.info/" + callsign + "/json"
        ).json()
        data = {
            "type": str(callsign_data["type"]),
            "class": str(callsign_data["current"]["operClass"]),
            "callsign": str(callsign_data["current"]["callsign"]),
            "name": str(callsign_data["name"]),
            "address": f'{callsign_data["address"]["line1"]}, {callsign_data["address"]["line2"]}',
            "location": f'Latitude: {callsign_data["location"]["latitude"]} Longitude: {callsign_data["location"]["longitude"]} Gridsquare: {callsign_data["location"]["gridsquare"]}',
            "otherInfo": f'FRN: {callsign_data["otherInfo"]["frn"]} Grant Date: {callsign_data["otherInfo"]["grantDate"]} Experation Date: {callsign_data["otherInfo"]["expiryDate"]}',
        }
    else:
        callsign = "Enter a Valid Callsign."

        data = {
            "type": str(" "),
            "class": str(" "),
            "callsign": str(" "),
            "name": str(" "),
            "address": str(" "),
            "location": str(" "),
            "otherInfo": str(" "),
        }

    print(data)
    return render_template("callsign.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
