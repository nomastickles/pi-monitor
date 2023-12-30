#!/bin/bash

if [[ $# != 3 ]]; then
  echo 'nohup ./notify_at_temp.sh "https://192.99.99.HI:4321/current?key=notsecure" "ntfy.sh/<topic string>" "63" \'
  echo '  >>"./data/MONITOR_NTFY_$(date +"%FT%H%M%S").log" 2>&1 & \'
  echo 'ps aux | grep NTFY_'
  exit 1
fi

HOST=$1
TOPIC=$2
TEMP=$3

while true; do
  RESULT=$(curl "$HOST" | jq '.DATA_ATMOSPHERE.TEMP_F')
  if (($(echo "$RESULT < $TEMP" | bc -l))); then
    echo "TOO COLD 🛟 $TEMP"
    curl -d $RESULT $TOPIC
    sleep 4
  else
    sleep 90
  fi

done
