from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request, abort
import os
import utils
import constants

load_dotenv(find_dotenv())

PATH_SSL_CRT = os.environ.get("PATH_SSL_CRT")
PATH_SSL_KEY = os.environ.get("PATH_SSL_KEY")
APP_SECRET = os.environ.get("APP_SECRET")

validation_schema = utils.get_validation_schema(APP_SECRET)
PORT = 8765
app = Flask(__name__)


@app.route("/update", methods=["GET"])
def update():
    errors = validation_schema.validate(request.args)
    if errors:
        abort(418)

    for input in constants.DATA_ITEMS:
        value = request.args.get(input)
        if value == None:
            continue
        if int(value) == 0:
            utils.clear_file(input)
        else:
            utils.write_file(input, value)
    return "ok"


@app.route("/current", methods=["GET"])
def current():
    errors = validation_schema.validate(request.args)
    if errors:
        abort(418)

    return utils.get_data()


@app.route("/", methods=["GET"])
def index():
    errors = validation_schema.validate(request.args)
    if errors:
        return abort(418)

    app_data = utils.get_data()
    app_data["KEY"] = APP_SECRET

    return render_template("index.html", app_data=app_data)


if __name__ == "__main__":
    context = None
    if not APP_SECRET:
        raise ValueError("😈")
    if PATH_SSL_CRT and PATH_SSL_KEY:
        print("🌈🔐 ssl_context")
        context = (PATH_SSL_CRT, PATH_SSL_KEY)
    app.run(host="0.0.0.0", port=PORT, debug=False, ssl_context=context)
