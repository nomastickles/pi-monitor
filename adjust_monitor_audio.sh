#!/bin/bash

# (To be used after ./start_monitor_audio.sh)
# This can adjust base loudness and sensitivity if you are not using monitor_ui stuff

# Examples:
# ./adjust_monitor_audio.sh "/tmp/pi-monitor-loudness-base" -50
# ./adjust_monitor_audio.sh "/tmp/pi-monitor-loudness-sensitivity" 60

if [[ $# != 2 ]]; then
  echo "need two arguments"
  exit 1
fi

if ! [[ $1 =~ ^/tmp/pi-monitor-*$ ]]; then
  echo "needs to be pi-monitor file"
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
  echo $VALUE >$FILE_TMP
  $(mv $FILE_TMP $FILE)
  $(rm $FILE_TMP)

done
