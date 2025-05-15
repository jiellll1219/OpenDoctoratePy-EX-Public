import re
import json

from flask import request
from random import shuffle
from constants import CONFIG_PATH
from collections import OrderedDict
from utils import read_json, write_json
from core.function.update import updateData


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
            version = updateData("https://ak-conf.hypergryph.com/config/prod/official/Android/version")
        elif mode == "global":
            version = updateData("https://ark-us-static-online.yo-star.com/assetbundle/official/Android/version")
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
    if mode == "cn":
        data = updateData("https://ak-conf.hypergryph.com/config/prod/announce_meta/Android/preannouncement.meta.json")
    elif mode == "global":
        data = updateData("https://ark-us-static-online.yo-star.com/announce/Android/preannouncement.meta.json")

    return data


def prodAnnouncement():

    server_config = read_json(CONFIG_PATH)
    mode = server_config["server"]["mode"]
    if mode == "cn":
        data = updateData("https://ak-conf.hypergryph.com/config/prod/announce_meta/Android/announcement.meta.json")    
    elif mode == "global":
        data = updateData("https://ark-us-static-online.yo-star.com/announce/Android/announcement.meta.json")

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