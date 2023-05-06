#!/bin/bash

LOG_FILE="/tmp/pi-monitor-atmosphere-$(date +"%FT%H%M%S").log"

nohup python ./backend/monitor_atmosphere.py \
  >>"$LOG_FILE" 2>&1 &

ps aux | grep monitor_atmosphere.py

ls -tpr /tmp/pi-monitor-atmosphere-* | tail -n 1
