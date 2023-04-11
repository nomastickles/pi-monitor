![](media/demo.gif)

![](media/demo-ui.gif)

DEMO: [https://nomastickles.github.io/pi-monitor/](https://nomastickles.github.io/pi-monitor/)

### What does this do

This is a python + react ui audio monitoring tool (indicative of baby monitoring tools that visually show loudness of a room) using a raspberry pi, usb microphone, and Philips Hue Bridge lights system.

The more sound the microphone picks up, the brighter the connected smart lights shine with sensitivity and base loudness adjustments (enabling tweaking the mic for the room).

What you need:

- rpi + usb microphone
- philips hue bridge light system on same local network as rpi
- (optional) DHT22 temperature + humidity sensor

```sh

# 1. clone the repo in your pi
# 2. install the deps

sudo apt update
sudo apt full-upgrade -y
sudo apt-get install -y libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev libatlas-base-dev

pip install pyaudio pyloudnorm python-dotenv marshmallow
pip install --upgrade numpy
pip install --upgrade Flask

# following should have “Class=Audio, Driver=snd-usb-audio”
lsusb -t
# 3. running get_audio_device_index will tell you the mic index is
python3 ./backend/get_audio_device_index.py

# 4. create/fill out ./backend/.env

# 5. then edit start_monitor_audio.sh with your mic index and other options
chmod a+x ./start_monitor_audio.sh && ./start_monitor_audio.sh
chomd a+x ./start_monitor_ui.sh && ./start_monitor_ui.sh

# if temperature sensor:
chomd a+x ./get_outside_atmosphere.sh ./get_outside_atmosphere.sh
```

### ./backend/.env

APP_SECRET = simple not very secure way to gate all flask APIs

BRIDGE_USERNAME = username from Hue bridge

BRIDGE_HOST=http://192.168.30.20

WEATHER_API_USER_AGENT_SECRET = used with api.weather.gov to get outside metrics
example: "(pi-monitor, your@email.com)"

### Phillips Hue bridge stuff

https://developers.meethue.com/develop/get-started-2/

You'll need to create a username and add to ./backend/.env

### (optional) api.weather.gov stuff

Please see https://www.weather.gov/documentation/services-web-api

Example cron:

```sh
2 * * * * python3 /home/pi/pi-monitor/backend/get_outside_atmosphere.py --weather-api-url https://api.weather.gov/gridpoints/SEW/130,68/forecast/hourly >> /tmp/pi-monitor-atmosphere-outside.log 2>&1

```

### TODO

- count nearby network mac addresses with Airodump-ng and save to file
- send all values of /tmp/pi-monitor files to managed grafana in aws

### Resources + Help

https://github.com/csteinmetz1/pyloudnorm

https://github.com/pklaus/pklaus/tree/master/pklaus/audio/level

https://github.com/tigoe/hue-control

https://github.com/adafruit/Adafruit_CircuitPython_DHT/blob/main/examples/dht_simpletest.py

https://www.weather.gov/documentation/services-web-api
