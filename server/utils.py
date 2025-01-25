import json
import hashlib
import requests

from msgspec.json import Encoder, Decoder, format
from os import path as ospath, makedirs
from hashlib import md5, sha3_512
from random import shuffle
from datetime import datetime, UTC
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from threading import Lock

json_encoder = Encoder(order="deterministic")
json_decoder = Decoder(strict=False)

with open("config/multiUserConfig.json") as f:
    multiUserConfig = json.load(f)
multiUserEnabled = multiUserConfig["enabled"]

users = {}
users_lock = Lock()

def read_json(path: str, **args):
    with open(path, **args) as f:
        return json.load(f)

def write_json(data, path: str, **args):
    with open(path, "w", **args) as f:
        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        f.write(json_data)

def decrypt_battle_data(data: str, login_time: int) -> dict:
    
    LOG_TOKEN_KEY = "pM6Umv*^hVQuB6t&"
    
    battle_data = bytes.fromhex(data[:len(data) - 32])
    src = LOG_TOKEN_KEY + str(login_time)
    key = hashlib.md5(src.encode()).digest()
    iv = bytes.fromhex(data[len(data) - 32:])
    aes_obj = AES.new(key, AES.MODE_CBC, iv)
    try:
        decrypt_data = unpad(aes_obj.decrypt(battle_data), AES.block_size)
        return json.loads(decrypt_data)
    
    except Exception as e:
        return None
    
def update_data(url):
    BASE_URL_LIST = [
        (
            "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata",
            "./data",
        ),
        (
            "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata",
            "./data-global",
        ),
        (
            "https://ak-conf.hypergryph.com/config/prod/announce_meta/Android",
            "./data/announce",
        ),
        (
            "https://ark-us-static-online.yo-star.com/announce/Android",
            "./data/announce",
        ),
    ]

    localPath = ""

    for index in BASE_URL_LIST:
        if index[0] in url:
            if not ospath.isdir(index[1]):
                makedirs(index[1])
            localPath = url.replace(index[0], index[1])
            break

    if not ospath.isdir("./data/excel/"):
        makedirs("./data/excel/")

    if "Android/version" in url:
        data = requests.get(url).json()
        return data
    current_is_mod = False

    if not current_is_mod:
        try:
            raise Exception
            data = requests.get(url).json()
            write_json(data, localPath)

        except Exception as e:
            logging(e)
            data = read_json(localPath, encoding="utf-8")
    else:
        data = read_json(localPath, encoding="utf-8")

    return data

def rand_name(len: int = 16) -> str:
    dt = datetime.now()
    time = (dt.year, dt.month, dt.day)
    seed = ""
    for t in time:
        seed += str(t)
    seed = str(shuffle(list(seed)))
    return sha3_512(seed.encode()).hexdigest()[:len]

def logging(data):
    name = rand_name(8)
    log_message = f"[{datetime.now(UTC).isoformat()}] {data}"
    print(log_message)
    with open(f"logs/{name}.log", "w") as f:
        f.write(log_message)