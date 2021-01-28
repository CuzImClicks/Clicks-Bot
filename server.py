from flask import Flask, url_for, redirect, request, jsonify, send_file
from web_server.database import *
from PIL import Image

server = Flask(__name__)

users = {"henrik": {"name": "henrik hoppe", "alter": 15}}


@server.route("/")
def index():
    return redirect(url_for("api_key"))


@server.route("/api/users", methods=["GET"])
def api_users():
    print(request.args)
    req = dict(request.args)
    try:
        key = req["key"]
    except KeyError:
        print({"success": False, "error": "No API-Key provided"})
        return jsonify({"success": False, "error": "No API-Key provided"})

    try:
        name = req["name"]

    except KeyError:
        print({"success": False, "error": "No name provided"})
        return jsonify({"success": False, "error": "No name provided"})

    try:
        user = users[req["name"]]

    except KeyError:
        print({"success": False, "error": "User not found"})
        return jsonify({"success": False, "error": "User not found"})

    if key and name and user:
        print(user, key)
        if check_key(key):
            return jsonify({"success": True, "user": user})

        else:
            return jsonify({"success": False, "error": "Invalid key provided"})

    else:
        return jsonify({"success": True, "error": "Internal error"})


@server.route("/api/key")
def api_key():

    print(request.args)
    req = dict(request.args)

    try:
        user_name = req["name"]

    except KeyError:
        return jsonify({"success": False, "error": "No name provided"})

    if not check_for_key(user_name):
        key = create_key(user_name)
        return jsonify({"success": True, "key": key})

    else:
        return jsonify({"success": False, "key": get_key(user_name)})


@server.route("/assets/steam_icon")
def steam_icon():

    req = dict(request.args)
    try:
        key = req["key"]
    except KeyError:
        print({"success": False, "error": "No API-Key provided"})
        return jsonify({"success": False, "error": "No API-Key provided"})

    return send_file(f"{os.getcwd()}/assets/steam_icon.jpg")


@server.route("/assets/Clicks-BotAPI")
def clicksapi_picture():

    req = dict(request.args)
    try:
        key = req["key"]
    except KeyError:
        print({"success": False, "error": "No API-Key provided"})
        return jsonify({"success": False, "error": "No API-Key provided"})

    return send_file(f"{os.getcwd()}/assets/Clicks-Bot API.jpg")


async def run(debug=False):
    server.run(debug=debug)
