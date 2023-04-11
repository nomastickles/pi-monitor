from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request, abort
import constants
import os
import utils

load_dotenv(find_dotenv())

APP_SECRET = os.environ.get("APP_SECRET")
validation_schema = utils.get_validation_schema(APP_SECRET)
PORT = 8765
app = Flask(__name__)


@app.route("/update", methods=["GET"])
def update():
    errors = validation_schema.validate(request.args)
    if errors:
        abort(418)

    if request.args.get("LOUDNESS_BASE"):
        utils.write_file(
            constants.FILE_LOUDNESS_BASE, request.args.get("LOUDNESS_BASE")
        )
    if request.args.get("LOUDNESS_SENSITIVITY"):
        utils.write_file(
            constants.FILE_LOUDNESS_SENSITIVITY,
            request.args.get("LOUDNESS_SENSITIVITY"),
        )
    return "ok"


@app.route("/current", methods=["GET"])
def current():
    errors = validation_schema.validate(request.args)
    if errors:
        abort(418)

    return {
        "LOUDNESS": utils.get_file_content(constants.FILE_LOUDNESS),
        "ATMOSPHERE": utils.get_file_content(
            filename=constants.FILE_ATMOSPHERE,
            if_modified_by_seconds=60,
            is_json=True,
        ),
    }


@app.route("/", methods=["GET"])
def index():
    errors = validation_schema.validate(request.args)
    if errors:
        return abort(418)

    app_data = {
        "LOUDNESS": utils.get_file_content(constants.FILE_LOUDNESS),
        "LOUDNESS_BASE": utils.get_file_content(constants.FILE_LOUDNESS_BASE),
        "LOUDNESS_SENSITIVITY": utils.get_file_content(
            constants.FILE_LOUDNESS_SENSITIVITY
        ),
        "ATMOSPHERE": utils.get_file_content(
            filename=constants.FILE_ATMOSPHERE,
            if_modified_by_seconds=60,
            is_json=True,
        ),
        "ATMOSPHERE_OUTSIDE": utils.get_file_content(
            filename=constants.FILE_ATMOSPHERE_OUTSIDE,
            if_modified_by_seconds=60 * 60 + 1,
            is_json=True,
        ),
        "KEY": APP_SECRET,
    }

    return render_template("index.html", app_data=app_data)


if __name__ == "__main__":
    if not APP_SECRET:
        raise ValueError("no APP_SECRET")
    app.run(host="0.0.0.0", port=PORT, debug=True)
