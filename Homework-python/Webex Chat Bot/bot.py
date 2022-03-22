import json
import os
from dotenv import load_dotenv
import requests
from flask import Flask, request

# Personal Details #
# Weather bot written for Incubator 2022

# Bot Details #
config = load_dotenv(".env")
bot_name = os.getenv("BOT_NAME")
token = os.getenv("TOKEN_API")
weather_api = os.getenv("WEATHER_API")

header = {"content-type": "application/json; charset=utf-8",
          "authorization": "Bearer " + token}

# Flask Application #
app = Flask(__name__)


@app.route("/", methods = ["GET", "POST"])
def send_message():
    webhook = request.json
    url = 'https://webexapis.com/v1/messages'
    msg = {"roomId": webhook["data"]["roomId"]}
    sender = webhook["data"]["personEmail"]
    message = get_message()
    if sender != bot_name:
        if message.lower() == "help":  # If message is help
            msg[
                "markdown"] = "Welcome to **Weather Bot**!  \n List of available commands: \n- weather \n- weather {" \
                              "City},{Country Code} \n- is it raining? \n- help"  # List all possible commands

        elif message.lower() == "weather":  # If message is weather
            msg[
                "markdown"] = "To use the weather functionality, you can also type in the command: \n weather {City}, " \
                              "" \
                              "" \
                              "" \
                              "" \
                              "" \
                              "" \
                              "{Country Code} \n Alternatively, this shows the approximate location based on your IP " \
                              "Address"  # List alternative use
            requests.post(url, data = json.dumps(msg), headers = header, verify = True)
            url_current_loc = "http://ip-api.com/json/"  # url for ip to location API
            url_current_loc_response = requests.get(url_current_loc, headers = header, verify = True)
            if url_current_loc_response.status_code == 200:  # If status code is 200
                url_current_loc_json = url_current_loc_response.json()  # Get JSON array
                city = url_current_loc_json["city"]  # get city
                country_code = url_current_loc_json["countryCode"]  # get country code
                url_weather = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "," + country_code + \
                              "&appid=" + weather_api  # url for weather API
                url_weather_response = requests.get(url_weather, headers = header, verify = True)
                get_weather_details(url_weather_response, msg, city, country_code, "full_details")  # Function call

        elif message.lower() == "is it raining?" or message.lower() == "is it raining":  # If message is: is it raining
            url_current_loc = "http://ip-api.com/json/"  # url for ip to location API
            url_current_loc_response = requests.get(url_current_loc, headers = header, verify = True)
            if url_current_loc_response.status_code == 200:  # if status code is 200
                url_current_loc_json = url_current_loc_response.json()  # Get JSON array
                city = url_current_loc_json["city"]  # get city
                country_code = url_current_loc_json["countryCode"]  # get country code
                url_weather = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "," + country_code + \
                              "&appid=" + weather_api  # url for weather API
                url_weather_response = requests.get(url_weather, headers = header, verify = True)
                get_weather_details(url_weather_response, msg, city, country_code, "is_it_raining_only")

        elif message.lower().split(" ")[0] == "weather":  # if first part of message is weather
            part = message.split(" ", 1)[1]  # Split
            part2 = part.split(",")  # Split
            # print(part2)
            city = part2[0]  # get city
            country_code = part2[1]  # get country code
            # print(city)
            # print(country_code)
            url_weather = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "," + country_code + \
                          "&appid=" + weather_api
            # print(url_weather)
            # print(url_weather)
            url_weather_response = requests.get(url_weather, headers = header, verify = True)
            get_weather_details(url_weather_response, msg, city, country_code, "full_details")  # function call

        else:  # message is not amongst the supported ones
            msg["markdown"] = "Sorry! I didn't recognize that command. Type **help** to see the list of available " \
                              "commands. "
        requests.post(url, data = json.dumps(msg), headers = header, verify = True)


def get_message():
    webhook = request.json
    url = 'https://webexapis.com/v1/messages/' + webhook["data"]["id"]
    get_msgs = requests.get(url, headers = header, verify = True)
    message = get_msgs.json()['text']
    return message


def get_weather_details(url_weather_response, msg, city, country_code, details):
    if details == "full_details":  # If asking for full details
        if url_weather_response.status_code == 200:  # if response is 200
            url_weather_json = url_weather_response.json()  # get json
            # print(url_weather_json)
            # Get variables from json
            temp_k = url_weather_json["main"]["temp"]
            temp_c = int(temp_k - 273.15)
            temp_feels_like_k = url_weather_json["main"]["feels_like"]
            temp_feels_like_c = int(temp_feels_like_k - 273.15)
            temp_min_k = url_weather_json["main"]["temp_min"]
            temp_min_c = int(temp_min_k - 273.15)
            temp_max_k = url_weather_json["main"]["temp_max"]
            temp_max_c = int(temp_max_k - 273.15)
            main = url_weather_json["weather"][0]["description"]
            msg[
                "markdown"] = "The weather in " + city.title() + ", " + country_code.upper() + " is: \n" + \
                              main.title() + \
                              "\n Current Temperature: " + str(temp_c) + "°C" + "\n Feels Like: " + str(
                temp_feels_like_c) + "°C" + "\n Min Temperature: " + \
                              str(temp_min_c) + "°C" + "\n Max Temperature: " + str(temp_max_c) + "°C"

        else:
            msg["markdown"] = "Sorry! It seems you have misspelled the name of the city or the country code \n " \
                              "Alternatively, the city you are looking for might not be available in the weather " \
                              "data "
    elif details == "is_it_raining_only":
        if url_weather_response.status_code == 200:
            url_weather_json = url_weather_response.json()
            main = url_weather_json["weather"][0]["main"]
            if main == "Thunderstorm" or main == "Drizzle" or main == "Rain":
                msg["markdown"] = "Yes :("
            else:
                msg["markdown"] = "No :)"


app.run(debug = True)
