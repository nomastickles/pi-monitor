#!/bin/bash

./start_monitor_atmosphere.sh
./start_monitor_audio.sh
./start_monitor_ui.sh

LOG_FILE_NV="/tmp/NV-$(date +"%FT%H%M%S").log"
nohup ./blink1_monitor_night_vision.sh >>"$LOG_FILE_NV" 2>&1 &
ls -tpr /tmp/NV-* | tail -n 1
