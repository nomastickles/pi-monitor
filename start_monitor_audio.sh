#!/bin/bash

# use get_audio_device_index.py to find the index of your audio device

LOG_FILE="/tmp/pi-monitor-audio-$(date +"%FT%H%M%S").log"

#  --bridge-light-names "Hue Go,Eat 1,Eat 2,Eat 3" \
nohup python ./backend/monitor_audio.py \
  --input-device-index 4 \
  --bridge-light-names "Hue Go,Hue Go Go" \
  --display-visual \
  --record-loudness \
  >>$LOG_FILE 2>&1 &

ps aux | grep monitor_audio.py

ls -tpr /tmp/pi-monitor-audio-* | tail -n 1
