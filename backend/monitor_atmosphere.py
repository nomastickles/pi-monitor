import adafruit_dht
import argparse
import board
import constants
import json
import logging
import time
import utils
import os
import time

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.

LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
logging.basicConfig(format="%(asctime)s %(message)s", level=LOGLEVEL)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--record-delay-seconds", default=5, type=int)
    parser.add_argument("--error-delay-seconds", default=3, type=int)
    args = parser.parse_args()

    first_time_check = True

    while True:
        try:
            # Print the values to the serial port
            temperature_c = dhtDevice.temperature
            temperature_f = round(temperature_c * (9 / 5) + 32, 1)
            humidity = round(dhtDevice.humidity, 1)

            if first_time_check:
                # the first go round always seems off
                first_time_check = False
                time.sleep(2)
                continue

            logging.debug(
                "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                    temperature_f, temperature_c, humidity
                )
            )

            # do we need to store both C and F? nope but whatevs
            data = {
                "TEMP_C": temperature_c,
                "TEMP_F": temperature_f,
                "HUMIDITY": humidity,
            }

            utils.write_file(constants.FILE_ATMOSPHERE, json.dumps(data))

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going

            logging.error(error.args[0])
            time.sleep(args.error_delay_seconds)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error
        except KeyboardInterrupt:
            print()

        time.sleep(args.record_delay_seconds)


if __name__ == "__main__":
    main()
