#!/bin/bash

# see https://github.com/todbot/blink1/blob/main/docs/blink1-tool-tips.md
# https://stackoverflow.com/questions/8654051/how-can-i-compare-two-floating-point-numbers-in-bash

if [ ! $# -eq 2 ]; then
  echo "two arumentents needed"
  echo "example: sh ./blink1_monitor_audio.sh "http://192.168.50.123:8765/current?key=someKey" -37"
  exit 1
fi

URL=$1
BASE_LOUDNESS=$2

./blink1-tool --off

while true; do
  RESULT=$(curl "$URL" | jq '.LOUDNESS' | bc)
  if (($(echo "$RESULT > $BASE_LOUDNESS" | bc -l))); then
    echo "$RESULT > $BASE_LOUDNESS"
    echo "---------------- 🔈🔉🔊 ⚡️"
    ./blink1-tool --magenta
  fi

  sleep 4
done
