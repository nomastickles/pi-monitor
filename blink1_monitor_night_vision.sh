#!/bin/bash

while [ true ]; do

  sleep 5
  FILE="/tmp/NIGHT_VISION"
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

  # now on
  if [[ "$NOTE" =~ .*"ON".* ]]; then
    continue
  fi

  echo "TURN IT ON"

  blink1-tool --millis 10000 -b 100 --red
  blink1-tool --writenote 8 --notestr 'ON'

done
