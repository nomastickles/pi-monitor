#!/bin/bash

sudo apt update
sudo apt full-upgrade -y
sudo apt install git -y
sudo apt-get install -y libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev libatlas-base-dev

pip install pyaudio pyloudnorm python-dotenv marshmallow
pip install --upgrade numpy
pip install --upgrade Flask

# 3. fill out ./backend/.env file
cp ./backend/.env-sample ./backend/.env

# following should have “Class=Audio, Driver=snd-usb-audio”
lsusb -t
# 4. running get_audio_device_index will tell you the mic index is
python3 ./backend/get_audio_device_index.py

chmod a+x start_monitor_audio.sh start_monitor_ui.sh start_monitor_atmosphere.sh start.sh

sudo apt install libudev-dev -y
git clone https://github.com/todbot/blink1-tool.git
cd ./blink1-tool && make
./blink1-tool --add_udev_rule
sudo cp blink1-tool /usr/local/bin
blink1-tool --millis 2000 -b 100 --green

sleep 5 && reboot
