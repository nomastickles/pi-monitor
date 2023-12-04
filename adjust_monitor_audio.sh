#!/bin/bash

# (To be used after ./backend/monitor_audio.py is running)
# This can adjust base loudness and sensitivity without monitor_ui stuff

# Examples:
# ./adjust_monitor_audio.sh "./data/pi-monitor-loudness-base" -50
# ./adjust_monitor_audio.sh "./data/pi-monitor-loudness-sensitivity" 60

if [[ $# != 2 ]]; then
  echo "need two arguments"
  exit 1
fi

if ! [[ $1 =~ ^./data/MONITOR_AUDIO_*$ ]]; then
  echo "needs audio monitoring"
fi

FILE=$1
FILE_TMP="$FILE-tmp"
VALUE=$2

if ! [ -f "$FILE" ]; then
  echo 'file does not exist'
  exit 2
fi

echo "press '<' and '>'"
echo "----"
echo "current: $VALUE"

while :; do
  read -n 1 k <&1

  case "$k" in
  ">" | ".")
    ((VALUE = $VALUE + 1))
    ;;
  "<" | ",")
    ((VALUE = $VALUE - 1))
    ;;
  "q")
    echo "quiting"
    exit 1
    ;;
  esac
  echo "$VALUE"
  echo "$VALUE > $FILE_TMP"
  mv "$FILE_TMP" "$FILE"
  rm "$FILE_TMP"

done
