#!/bin/bash

# 64bit Debian Bookworm Raspberry Pi 4

apt-get update -y
apt-get upgrade -y

sudo apt install -y portaudio19-dev python3-flask jq

python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt

# 3. be sure to fill this out
cp ./backend/.env-sample ./backend/.env

# following should have “Class=Audio, Driver=snd-usb-audio”
lsusb -t | snd-usb-audio

# 4. running get_audio_device_index will tell you the mic index is
python3 ./backend/get_audio_device_index.py | grep "Input Device id"

# sudo apt install libudev-dev -y
# git clone https://github.com/todbot/blink1-tool.git
# cd ./blink1-tool && make
# ./blink1-tool --add_udev_rule
# sudo cp blink1-tool /usr/local/bin
# blink1-tool --millis 2000 -b 100 --green

# sleep 5 && reboot
