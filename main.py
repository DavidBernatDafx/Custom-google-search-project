
# imports
from flask import Flask, render_template, request, send_file, flash
from flask_apscheduler import APScheduler
import requests
from markupsafe import escape
import json
import os
from dotenv import load_dotenv
import datetime
import random

# lead and set constants
load_dotenv(os.path.join(os.getcwd(), "_env", ".env"))
KEY = os.getenv("KEY")
CX = os.getenv("CX")


def make_api_call(keyword: str):
    """
    Function that makes googleApis api call for search keyword and returns tuple(data, images, error)
    """
    # api call parameters
    params = {
        "key": KEY,
        "q": keyword,
        "cx": CX,
    }

    data = None
    images = None
    error = False

    # api call
    with requests.get("https://www.googleapis.com/customsearch/v1", params=params) as response:
        if not response.status_code == 429:

            # creating and tapping response json
            data = response.json()
            try:
                data = data["items"]
            except (IndexError, KeyError):
                data = []
            else:
                # images are passed to template separately due to not every result has an image
                images = []
                for img in data:
                    try:
                        images.append(img["pagemap"]["metatags"][0]["og:image"])
                    except KeyError:
                        images.append("No image")

        else:
            error = True

    return data, images, error


def save_to_cache(keyword: str, data: list):
    """
    Function that creates unique filepath and saves the api call json (already stripped and modified) to cache
    folder. Function returns full filepath
    """

    cache_path = os.path.join(os.getcwd(), "cache")
    rnd_id = str(random.random()).split(".")[1]
    filename = f"results_{keyword}_{rnd_id}.json"
    full_path = os.path.join(cache_path, filename)

    with open(full_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=True, indent=4)

    return full_path


# instantiating flask app and BG task scheduler
app = Flask(__name__)
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

app.secret_key = os.getenv("APP_KEY")


@app.route("/", methods=["get", "post"])
def index():
    """
    Decorated Flask Function that returns rendered html template index.html
    """

    # setting variables
    year = (datetime.datetime.now()).strftime(format="%Y")
    full_path = None

    # check method
    if request.method == "POST":

        # defining searched keyword
        keyword = escape(request.form["search"])

        # make API call
        data, images, error = make_api_call(keyword)

        if not error:
            # save file and returns filepath
            full_path = save_to_cache(keyword, data)

        else:
            # set up flash message to be displayed to user
            flash("Too Many Requests. Try it again later.", category="error")

        return render_template("index.html",
                               data=data,
                               keyword=keyword,
                               images=images,
                               json_path=full_path,
                               year=year)

    else:
        return render_template("index.html", year=year
                               )


@app.route("/save/<path:json_path>")
def save(json_path):
    """
    Function that lets user save file by pdf filepath as pre-created pdf file.
    """

    return send_file(path_or_file=json_path, as_attachment=True)


@scheduler.task("cron", id="my_task", minute="*")
def check_old_files():
    """
    Scheduler function that runs on the background in the given interval, and removes all files from cache directory
    if file's date modified is older than 1 hour
    """
    # setting variables
    cache_path = os.path.join(os.getcwd(), "cache")
    now = datetime.datetime.now()

    # walk through files in cache folder
    for _, _, files in os.walk(cache_path):
        for file in files:

            file_path = os.path.join(cache_path, file)
            timestamp = os.path.getmtime(os.path.join(cache_path, file))
            date_modified = datetime.datetime.fromtimestamp(timestamp)

            # check date modified and if older than 1 hour delete it
            if now - date_modified > datetime.timedelta(hours=1):
                print("OLD")
                # safety measure, to not crash app itself with error
                if os.path.isfile(file_path):
                    os.remove(file_path)
            else:
                print("NEW")


# running app
if __name__ == "__main__":
    app.run(debug=True)
