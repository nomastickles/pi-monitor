#!/usr/bin/env python

"""
Copied stuff from
https://github.com/pklaus/pklaus/tree/master/pklaus/audio/level
using this rad library
https://github.com/csteinmetz1/pyloudnorm

So what's the deal here?



"""
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import argparse
import constants
import logging
import math
import mute_alsa
import numpy
import os
import pyaudio
import pyloudnorm
import threading
import utils

load_dotenv(find_dotenv())

LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(format="%(asctime)s %(message)s", level=LOGLEVEL)


def main():
    bridge_username = os.environ.get("BRIDGE_USERNAME")
    bridge_host = os.environ.get("BRIDGE_HOST")

    parser = argparse.ArgumentParser()
    parser.add_argument("--input-device-index", required=True, type=int)
    parser.add_argument("--sample-rate", default=44100, type=int)
    parser.add_argument("--base-loudness", default=-30, type=int)
    parser.add_argument("--update-delay-seconds", default=10, type=int)
    parser.add_argument("--bridge-light-names", default="", type=str)
    parser.add_argument("--light-brightness-sensitivity", default=110, type=int)
    parser.add_argument("--light-brightness-padding", default=0, type=int)
    parser.add_argument("--lights-off-delay-seconds", default=2, type=int)
    parser.add_argument(
        "--light-brightness-logarithmic-sensitivity",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument(
        "--display-visual", action=argparse.BooleanOptionalAction, default=False
    )
    parser.add_argument(
        "--record-loudness", action=argparse.BooleanOptionalAction, default=False
    )
    parser.add_argument("--record-delay-seconds", default=5, type=int)
    args = parser.parse_args()

    should_turn_off_lights = True  # init  reset
    bridge_light_names = args.bridge_light_names
    can_update_lights = bool(bridge_username and bridge_host and bridge_light_names)
    bridge_url_base = ""
    light_ids_found = set()

    if can_update_lights:
        bridge_url_base = f"{bridge_host}/api/{bridge_username}"
        light_ids_found = utils.lights_init(bridge_url_base, bridge_light_names)

    peak_loudness = utils.get_peak_loudness_reset()

    base_loudness = (
        utils.get_file_content(filename=constants.DATA_LOUDNESS_BASE, is_int=True)
        or args.base_loudness
    )
    light_brightness_logarithmic_multiplier = (
        utils.get_file_content(
            filename=constants.DATA_LOUDNESS_SENSITIVITY, is_int=True
        )
        or args.light_brightness_sensitivity
    )

    # writing to files now ensures a values are set
    utils.write_file(constants.DATA_LOUDNESS_BASE, str(base_loudness))
    utils.write_file(
        constants.DATA_LOUDNESS_SENSITIVITY,
        str(light_brightness_logarithmic_multiplier),
    )

    datetime_delay_turn_off_lights = datetime.now()
    datetime_delay_record_loudness_to_file = utils.get_future_datetime(
        args.record_delay_seconds
    )
    datetime_delay_update_values_from_files = utils.get_future_datetime(
        args.update_delay_seconds
    )

    if can_update_lights and not len(light_ids_found):
        can_update_lights = False

    logging.info(
        f"light ids: {light_ids_found} | Sensitivity: {light_brightness_logarithmic_multiplier} | Base loudness: {base_loudness}"
    )

    frames_per_buffer = int(constants.BLOCK_SIZE_IN_SECONDS * args.sample_rate)
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=args.sample_rate,
        input_device_index=args.input_device_index,
        input=True,
        frames_per_buffer=frames_per_buffer,
    )
    meter = pyloudnorm.Meter(
        args.sample_rate, block_size=constants.BLOCK_SIZE_IN_SECONDS
    )
    # my_high_pass = pyloudnorm.IIRfilter(0.0, 0.5, 20.0, args.sample_rate, "high_pass")
    # my_high_shelf = pyloudnorm.IIRfilter(2.0, 0.7, 1525.0, args.sample_rate, "high_shelf")
    # meter._filters = {"my_high_pass": my_high_pass, "my_high_shelf": my_high_shelf}

    try:
        while not utils.check_for_halt():
            data = numpy.frombuffer(
                stream.read(frames_per_buffer, exception_on_overflow=False),
                dtype=numpy.float32,
            )

            # loudness is negative and increases to zero
            loudness: float = round(meter.integrated_loudness(data), 2)  # LUFS

            if should_turn_off_lights and utils.has_datetime_elapsed(
                datetime_delay_turn_off_lights
            ):
                # setting brightness to 0 turns off the lights
                utils.lights_update_all(bridge_url_base, light_ids_found, 0)
                should_turn_off_lights = False

            if utils.has_datetime_elapsed(datetime_delay_update_values_from_files):
                base_loudness = (
                    utils.get_file_content(
                        filename=constants.DATA_LOUDNESS_BASE,
                        if_modified_by_seconds=args.update_delay_seconds,
                        is_int=True,
                    )
                    or base_loudness
                )
                light_brightness_logarithmic_multiplier = (
                    utils.get_file_content(
                        filename=constants.DATA_LOUDNESS_SENSITIVITY,
                        if_modified_by_seconds=args.update_delay_seconds,
                        is_int=True,
                    )
                    or light_brightness_logarithmic_multiplier
                )
                datetime_delay_update_values_from_files = utils.get_future_datetime(
                    args.update_delay_seconds
                )

            if loudness > peak_loudness:
                peak_loudness = loudness

            if args.record_loudness and utils.has_datetime_elapsed(
                datetime_delay_record_loudness_to_file
            ):
                threading.Thread(
                    target=utils.write_file,
                    args=(constants.DATA_LOUDNESS, str(peak_loudness)),
                ).start()

                peak_loudness = utils.get_peak_loudness_reset()
                datetime_delay_record_loudness_to_file = utils.get_future_datetime(
                    args.record_delay_seconds
                )

            if loudness <= base_loudness:
                continue

            datetime_delay_turn_off_lights = utils.get_future_datetime(
                args.lights_off_delay_seconds
            )

            percentage = 1.00 - (peak_loudness / base_loudness)

            if percentage <= 0.00:
                continue

            light_brightness: int = min(
                math.trunc(constants.BRIGHTNESS_MAX * percentage)
                + args.light_brightness_padding,
                constants.BRIGHTNESS_MAX,
            )

            if light_brightness <= 0:
                continue

            light_brightness_logarithmic = min(
                math.trunc(
                    math.log10(light_brightness)
                    * light_brightness_logarithmic_multiplier
                ),
                constants.BRIGHTNESS_MAX,
            )

            if can_update_lights:
                light_brightness_outgoing = light_brightness

                if (
                    args.light_brightness_logarithmic_sensitivity
                    and not light_brightness_logarithmic_multiplier == 0
                ):
                    light_brightness_outgoing = light_brightness_logarithmic

                utils.lights_update_all(
                    bridge_url_base, light_ids_found, light_brightness_outgoing
                )
                should_turn_off_lights = True

            if not args.display_visual:
                logging.info(
                    f"{loudness} | {light_brightness} | {light_brightness_logarithmic}"
                )
                continue

            level = constants.LEVEL_CHAR * math.trunc(light_brightness / 2) + " "
            logging.info(
                f"{level}{loudness} | {light_brightness} | {light_brightness_logarithmic}"
            )

    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    main()
