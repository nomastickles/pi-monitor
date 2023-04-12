#!/bin/bash

LOG_FILE="/tmp/pi-monitor-ui-$(date +"%FT%H%M%S").log"
FLASK_DEBUG=1

nohup python ./backend/monitor_ui.py \
  >>$LOG_FILE 2>&1 &

ps aux | grep monitor_ui.py

VAR=$(ls -tpr /tmp/pi-monitor-ui-* | tail -n 1) && echo $VAR
