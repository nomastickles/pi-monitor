#!/bin/bash

# TODO: change LIGHTS to be dynamic / file based

# if [ -z "$LIGHTS" ]; then
#   echo "Must provide LIGHTS in environment" 1>&2
#   exit 1
# fi

LIGHTS="Hue Go,Hue Go Go"

# FLASK_DEBUG=1

# reset logs
rm ./data/MONITOR_*

source myenv/bin/activate

MIC_INFO=$(python3 ./backend/get_audio_device_index.py | grep "USB Audio")
MIC_DEVICE_INDEX=$(echo "$MIC_INFO" | awk '{print substr($0, 17, 1)}')

if [ -z "$MIC_DEVICE_INDEX" ]; then
  echo "MIC_DEVICE_INDEX not found" 1>&2
  exit 1
fi

# nohup python ./backend/monitor_atmosphere.py \
#   >>"./data/MONITOR_ATMOSPHERE_$(date +"%FT%H%M%S").log" 2>&1 &
# ps aux | grep monitor_atmosphere.py

# TODO: add .env values as args taken from exported shell variables
nohup python ./backend/monitor_audio.py \
  --input-device-index $MIC_DEVICE_INDEX \
  --bridge-light-names "$LIGHTS" \
  --display-visual \
  --record-loudness \
  >>"./data/MONITOR_AUDIO_$(date +"%FT%H%M%S").log" 2>&1 &
ps aux | grep monitor_audio.py

nohup python ./backend/monitor_ui.py \
  >>"./data/MONITOR_UI_$(date +"%FT%H%M%S").log" 2>&1 &
ps aux | grep monitor_ui.py

nohup ./led_monitor_night_vision.sh \
  >>"./data/MONITOR_NIGHT_VISION_$(date +"%FT%H%M%S").log" 2>&1 &
ps aux | grep VISION_

ls -lt data
