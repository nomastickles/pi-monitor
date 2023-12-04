"""
https://www.weather.gov/documentation/services-web-api

https://api.weather.gov/gridpoints/MPX/105,72/forecast/hourly

"""
from dotenv import load_dotenv, find_dotenv
import requests
import argparse
import constants
import json
import logging
import utils
import os

LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
logging.basicConfig(format="%(asctime)s %(message)s", level=LOGLEVEL)


def main():
    load_dotenv(find_dotenv())

    parser = argparse.ArgumentParser()
    parser.add_argument("--weather-api-url", type=str)
    args = parser.parse_args()

    user_agent_secret = os.environ.get("WEATHER_API_USER_AGENT_SECRET")

    if not user_agent_secret:
        logging.error("no user agent found")
        return

    headers = {"User-Agent": user_agent_secret}

    try:
        logging.info(args.weather_api_url)
        response = requests.get(args.weather_api_url, headers=headers)
        logging.info(response.status_code)

        temperature_f = response.json()["properties"]["periods"][0]["temperature"]
        temperature_c = round(((temperature_f - 32) / (9 / 5)), 1)
        humidity = response.json()["properties"]["periods"][0]["relativeHumidity"][
            "value"
        ]

        data = {
            "TEMP_C": temperature_c,
            "TEMP_F": temperature_f,
            "HUMIDITY": humidity,
        }

        data_string = json.dumps(data)
        utils.write_file(constants.DATA_ATMOSPHERE_OUTSIDE, data_string)
        logging.debug(data_string)

    except Exception as error:
        logging.error(error)


if __name__ == "__main__":
    main()
