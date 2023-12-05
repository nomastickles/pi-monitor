#!/bin/bash

echo "INIT"

while [ true ]; do

  sleep 5
  FILE="./data/DATA_NIGHT_VISION_LEVEL"
  COLOR="red"
  NOTE=$(blink1-tool --readnote 8)

  if ! [ -f "$FILE" ]; then
    if [[ "$NOTE" =~ .*"OFF".* ]]; then
      continue
    fi

    echo "TURN IT OFF"

    blink1-tool --millis 2000 --off
    blink1-tool --writenote 8 --notestr 'OFF'

    continue
  fi

  BRIGHTNESS=$(cat ./data/DATA_NIGHT_VISION_LEVEL)

  if [[ "$NOTE" =~ .*"ON $BRIGHTNESS $COLOR".* ]]; then
    continue
  fi

  echo "blink1-tool --millis 6000 -b $BRIGHTNESS --$COLOR"
  blink1-tool --millis 10000 -b $BRIGHTNESS --$COLOR
  blink1-tool --writenote 8 --notestr "ON $BRIGHTNESS $COLOR"

done
