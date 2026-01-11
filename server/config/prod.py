import re
import json
import requests

from flask import request
from random import shuffle
from constants import CONFIG_PATH
from utils import read_json, write_json


def randomHash():

    hash  = list("abcdef")
    shuffle(hash)

    return ''.join(hash)


def prodRefreshConfig():

    data = {
        "resVersion": None
    }

    return data, 200


def prodAndroidVersion():

    server_config = read_json(CONFIG_PATH)
    version = server_config["version"]["android"]

    if server_config["assets"]["enableMods"]:
        version["resVersion"] = version["resVersion"][:18] + randomHash()

    return version


def prodNetworkConfig():

    server_config = read_json(CONFIG_PATH)

    mode = server_config["server"]["mode"]
    server = request.host_url[:-1]
    network_config = server_config["networkConfig"][mode]
    funcVer = network_config["content"]["funcVer"]

    if server_config["assets"]["autoUpdate"]:
        if mode == "cn":
            version = requests.get("https://ak-conf.hypergryph.com/config/prod/official/Android/version")
        elif mode == "global":
            version = requests.get("https://ark-us-static-online.yo-star.com/assetbundle/official/Android/version")
        server_config["version"]["android"] = version

        write_json(server_config, CONFIG_PATH)

    for index in network_config["content"]["configs"][funcVer]["network"]:
        url = network_config["content"]["configs"][funcVer]["network"][index]
        if isinstance(url, str) and url.find("{server}") >= 0:
            network_config["content"]["configs"][funcVer]["network"][index] = re.sub("{server}", server, url)

    network_config["content"] = json.dumps(network_config["content"])

    return json.dumps(network_config)


def prodRemoteConfig():

    remote = read_json(CONFIG_PATH)["remote"]

    return json.dumps(remote)


def prodPreAnnouncement():

    server_config = read_json(CONFIG_PATH)
    mode = server_config["server"]["mode"]
    match mode:
        case "cn":
            data = requests.get("https://ak-conf.hypergryph.com/config/prod/announce_meta/Android/preannouncement.meta.json")
        case "global":
            data = requests.get("https://ark-us-static-online.yo-star.com/announce/Android/preannouncement.meta.json")
        case _:
            data = requests.get("https://ak-conf.hypergryph.com/config/prod/announce_meta/Android/preannouncement.meta.json")

    return data


def prodAnnouncement():

    server_config = read_json(CONFIG_PATH)
    mode = server_config["server"]["mode"]
    match mode:
        case "cn":
            data = requests.get("https://ak-conf.hypergryph.com/config/prod/announce_meta/Android/preannouncement.meta.json")
        case "global":
            data = requests.get("https://ark-us-static-online.yo-star.com/announce/Android/preannouncement.meta.json")
        case _:
            data = requests.get("https://ak-conf.hypergryph.com/config/prod/announce_meta/Android/preannouncement.meta.json")

    return data

def prodGateMeta():
    return {
        "preAnnounceId": "478",
        "actived": True,
        "preAnnounceType": 2
    }

def get_latest_game_info():

    server_config = read_json(CONFIG_PATH)
    mode = server_config["server"]["mode"]
    match mode:
        case "cn":
            version = server_config["version"]["android"]
        case "global":
            version = server_config["versionGlobal"]["android"]
        case _:
            version = server_config["version"]["android"]
    funcVer = server_config["networkConfig"][mode]["content"]["funcVer"]

    main_version  = funcVer.lstrip("V").lstrip("0") or "0"[:2]
    
    # result = OrderedDict([
    #     ("version", ""),
    #     ("action", 3),
    #     ("update_type", 0),
    #     ("update_info", OrderedDict([
    #         ("package", None),
    #         ("patch", None),
    #         ("custom_info", ""),
    #         ("source_package", None),
    #     ])),
    #     ("client_version", "")
    # ])

    result = {
        "version": f"{main_version}.0.0",
        "action": 0,
        "update_type": 0,
        "update_info": {
            "package": None,
            "patch": None,
            "custom_info": "",
            "source_package": None
        },
        "client_version": version["clientVersion"]
    }

    return result

def ak_sdk_config():
    return {"report_device_info": 10000}

def prodGameBulletin():
    # return redirect("https://ak-webview.hypergryph.com/gameBulletin")
    return """
    <!doctype html>
    <html lang="zh-cn">
    
    <head>
        <meta name="referrer" content="no-referrer">
        <meta charset="utf-8">
        <meta http-equiv="pragma" content="no-cache">
        <meta http-equiv="cache-control" content="no-cache">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <meta name="renderer" content="webkit">
        <meta name="force-rendering" content="webkit">
        <meta name="viewport" content="user-scalable=no,initial-scale=1,maximum-scale=1,minimum-scale=1,width=device-width,height=device-height,viewport-fit=cover">
        <meta name="copyright" content="Hypergryph">
        <meta name="format-detection" content="telephone=no,email=no,address=no">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="robots" content="noindex">
        <title>公告 | 明日方舟 - Arknights</title>
        <link href="https://web.hycdn.cn/arknights/webview/favicon.ico" rel="icon">
        <link as="image" href="https://web.hycdn.cn/arknights/webview/assets/img/header.bb67d4.png" rel="preload">
        <link as="image" href="https://web.hycdn.cn/arknights/webview/assets/img/rhodes.739d79.png" rel="preload">
        <link href="https://web.hycdn.cn/arknights/webview/commons.5dd297.css" rel="stylesheet">
        <link href="https://web.hycdn.cn/arknights/webview/game.77fefb.css" rel="stylesheet">
    </head>
    
    <body>
        <div id="root">
        </div>
        <script crossorigin="anonymous" src="https://web.hycdn.cn/arknights/webview/analytics.1585a3.js">
        </script>
        <script crossorigin="anonymous" src="https://web.hycdn.cn/arknights/webview/game_i18n.bb363a.js">
        </script>
        <script crossorigin="anonymous" src="https://web.hycdn.cn/arknights/webview/react.0bb887.js">
        </script>
        <script crossorigin="anonymous" src="https://web.hycdn.cn/arknights/webview/commons.cd79f1.js">
        </script>
        <script crossorigin="anonymous" src="https://web.hycdn.cn/arknights/webview/game.130b53.js">
        </script>
    </body>

    </html>
    """

def prodAnalyticsCollect():
    return {
        "status": 0,
        "code": 0,
        "msg": "",
        "data": {}
    }

def prodBulletinList(subpath):
    if subpath.startswith("bulletinList"):
        response = requests.get("https://ak-webview.hypergryph.com/api/game/bulletinList?target=Android")
    else:
        response = requests.get(f"https://ak-webview.hypergryph.com/api/game/{subpath}")

    return response.json()