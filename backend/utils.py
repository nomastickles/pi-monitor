from datetime import datetime, timedelta
from marshmallow import Schema, fields
from marshmallow.validate import Range, Equal
import constants
import os
import requests
import threading
import json
from typing import Union
import numpy


PATH_DATA = "/tmp/"


def check_for_halt() -> bool:
    if os.path.exists(PATH_DATA + constants.FILE_HALT):
        return True
    return False


def get_future_datetime(seconds: int) -> datetime:
    return datetime.now() + timedelta(seconds=seconds)


def has_datetime_elapsed(datetime_incoming: datetime) -> bool:
    if (datetime_incoming - datetime.now()).total_seconds() > 0:
        return False
    return True


def write_file(filename: str, content: str) -> None:
    file_temp = f"{filename}-temp"
    with open(PATH_DATA + file_temp, "w") as file:
        file.write(content)
    os.rename(PATH_DATA + file_temp, filename)


def clear_file(filename: str) -> None:
    if os.path.exists(PATH_DATA + filename):
        os.remove(PATH_DATA + filename)


def lights_init(bridge_url_base: str, light_targets: str) -> set:
    light_ids_found = set()
    light_targets = light_targets.split(",")
    try:
        url = f"{bridge_url_base}/lights"
        payload = {"on": False}
        response = requests.get(url, json=payload)
        for id in response.json():
            light_name = response.json()[id]["name"]
            if not light_name in light_targets:
                continue
            if not response.json()[id]["state"]["reachable"]:
                continue
            light_ids_found.add(id)
    finally:
        return light_ids_found


def light_update(bridge_url_base: str, id: str, brightness: int = 0) -> None:
    url = f"{bridge_url_base}/lights/{id}/state"
    if brightness == 0:
        requests.put(
            url,
            json={
                "on": False,
            },
        )
        return
    requests.put(
        url,
        json={
            "on": True,
            "bri": brightness,
        },
    )


def lights_update_all(
    bridge_url_base: str, light_ids_found: set, brightness: int = 0
) -> None:
    for id in light_ids_found:
        light_update(bridge_url_base, id, brightness)


def lights_update_all_OLD(
    bridge_url_base: str, light_ids_found: set, brightness: int = 0
) -> None:
    for id in light_ids_found:
        threading.Thread(
            target=light_update, args=(bridge_url_base, id, brightness)
        ).start()


def get_peak_loudness_reset() -> float:
    return float("-inf")


def get_file_content(
    filename: str,
    if_modified_by_seconds: int = numpy.inf,
    is_json=False,
    is_int=False,
) -> Union[str, None]:
    if not os.path.exists(PATH_DATA + filename):
        return None
    modified_timestamp = os.path.getmtime(PATH_DATA + filename)
    if (
        datetime.now() - datetime.fromtimestamp(modified_timestamp)
    ).total_seconds() > if_modified_by_seconds:
        return None
    with open(PATH_DATA + filename, "r") as f:
        results = f.read()
        if results == "":
            return None
        if is_int:
            return int(results)
        if is_json:
            return json.loads(results)
        return results


def get_validation_schema(incomingKey: str):
    class update_input_schema(Schema):
        key = fields.Str(required=True, validate=Equal(incomingKey))
        LOUDNESS_BASE = fields.Int(required=False, validate=Range(min=-80, max=0))
        LOUDNESS_SENSITIVITY = fields.Int(
            required=False, validate=Range(min=0, max=250)
        )
        NIGHT_VISION = fields.Int(required=False, validate=Range(min=0, max=1))

    return update_input_schema()


def get_data():
    app_data = {}

    for item in constants.DATA_ITEMS:
        value = ""

        if item == constants.FILE_ATMOSPHERE:
            value = get_file_content(
                filename=item,
                if_modified_by_seconds=60,
                is_json=True,
            )
            continue

        if item == constants.FILE_ATMOSPHERE_OUTSIDE:
            value = get_file_content(
                filename=item,
                if_modified_by_seconds=60 * 60 + 1,
                is_json=True,
            )
            continue

        value = get_file_content(item)

        if value == None:
            continue
        app_data[item] = value

    return app_data
