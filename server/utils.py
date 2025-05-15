import json
import hashlib
import requests
import traceback
import sys

from msgspec.json import Encoder, Decoder
from os import path as ospath, makedirs
from hashlib import sha3_512
from random import shuffle
from flask import after_this_request
from datetime import datetime, UTC
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from concurrent.futures import ThreadPoolExecutor

from threading import Lock

from constants import USER_JSON_PATH

json_encoder = Encoder(order="deterministic")
json_decoder = Decoder(strict=False)

with open("config/multiUserConfig.json") as f:
    multiUserConfig = json.load(f)
multiUserEnabled = multiUserConfig["enabled"]

users = {}
users_lock = Lock()

def read_json(path: str, **args):
    if 'b' not in args.get('mode', ''):
        args.setdefault('encoding', 'utf-8')
    with open(path, **args) as f:
        return json.load(f)

def write_json(data, path: str, **args):
    if 'b' not in args.get('mode', ''):
        args.setdefault('encoding', 'utf-8')
    with open(path, "w", **args) as f:
        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        f.write(json_data)

def decrypt_battle_data(data: str, login_time: int = read_json(USER_JSON_PATH)["user"]["pushFlags"]["status"]):
    
    LOG_TOKEN_KEY = "pM6Umv*^hVQuB6t&"
    
    battle_data = bytes.fromhex(data[:len(data) - 32])
    src = LOG_TOKEN_KEY + str(login_time)
    key = hashlib.md5(src.encode()).digest()
    iv = bytes.fromhex(data[len(data) - 32:])
    aes_obj = AES.new(key, AES.MODE_CBC, iv)
    try:
        decrypt_data = unpad(aes_obj.decrypt(battle_data), AES.block_size)
        return json.loads(decrypt_data)
    except Exception:
        return {}
    
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

executor = ThreadPoolExecutor(max_workers=10)
# 线程池最大数量，默认为10
def run_after_response(func, *args, on_error=None, sequential=False):
    """
    在函数返回后异步执行函数（带线程池、异常捕获）。

    :param func: 要执行的函数。支持带一个参数(data)，亦可以无参数。
    :param *args: 可选，传给函数的参数/数据。
    :param on_error: 可选，异常回调函数。例子: on_error(exception, traceback_str)
    """
    @after_this_request
    def register(response):
        def task():
            try:
                func(*args)
            except Exception as e:
                tb_str = traceback.format_exc()
                if on_error:
                    on_error(e, tb_str)
                else:
                    print(f"[处理异常] {e}", file=sys.stderr)
                    print(tb_str, file=sys.stderr)
        
        executor.submit(task)
        return response