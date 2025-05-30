import json
import hashlib
import requests
import traceback
import sys
import os

from msgspec.json import Encoder, Decoder
from typing import Dict, Any
from datetime import datetime, timezone
from os import path as ospath, makedirs
from hashlib import sha3_512
from random import shuffle
from flask import after_this_request
from datetime import datetime, UTC
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from concurrent.futures import ThreadPoolExecutor

from threading import Lock

from constants import USER_JSON_PATH, EX_CONFIG_PATH, SERVER_DATA_PATH

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
    
#定义一个全局变量，用于存储从 JSON 文件中读取的数据
memory_cache: Dict[str, Any] = {}
# 读取 JSON 文件并存入内存
def preload_json_data():
    # 加载 data/excel 目录下的所有 JSON 文件到内存中
    global memory_cache
    excel_dir = "data/excel"
    
    # 确保目录存在
    if not os.path.exists(excel_dir):
        raise FileNotFoundError(f"未找到目录: {excel_dir}")
    
    # 遍历目录下的所有 JSON 文件
    for filename in os.listdir(excel_dir):
        if filename.endswith(".json"):
            # 去除 .json 后缀作为 key
            key = filename[:-5]
            file_path = os.path.join(excel_dir, filename)
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    memory_cache[key] = Decoder(strict=False).decode(f.read())
            except Exception as e:
                print(f"加载 {filename} 失败: {str(e)}")

def get_memory(key: str):
    useMemoryCache = read_json(EX_CONFIG_PATH)["useMemoryCache"]
    if useMemoryCache:
        try:
            return memory_cache.get(key)
        except Exception:
            print("Error: Failed to load {key} from memory")
            return read_json(f"data/excel/{key}.json")
    else:
        return read_json(f"data/excel/{key}.json", encoding='utf-8')

def update_check_in_status():
    default_data = {
        "lastCheckInTs": 0,
        "lastResetDate": "2000-01-01"
    }
    
    server_data = read_json(SERVER_DATA_PATH)
    user_data = read_json(USER_JSON_PATH)
    
    check_in_data = server_data.get("checkInData", default_data)
    
    # 获取当前时间（设备本地时区）
    now_local = datetime.now().astimezone()
    today_date = now_local.date()
    
    # 处理lastResetDate
    last_reset_date = datetime.strptime(
        check_in_data["lastResetDate"], "%Y-%m-%d"
    ).date()
    
    # 计算今天的4AM（本地时区）
    today_4am = datetime.combine(today_date, datetime.min.time()).replace(
        hour=4, minute=0, second=0, microsecond=0
    ).astimezone(now_local.tzinfo)
    
    # 处理签到时间戳
    last_check_in_ts = check_in_data["lastCheckInTs"]
    
    # 转换时间戳为datetime对象
    if isinstance(last_check_in_ts, int) and last_check_in_ts > 0:
        last_check_in_dt = datetime.fromtimestamp(last_check_in_ts, tz=now_local.tzinfo)
    elif isinstance(last_check_in_ts, str):
        last_check_in_dt = datetime.fromisoformat(last_check_in_ts)
    else:  # 包括lastCheckInTs=0的情况
        last_check_in_dt = datetime.min.replace(tzinfo=timezone.utc).astimezone(now_local.tzinfo)
    
    # 条件1: 当前时间已经过了今天4AM
    condition1 = now_local >= today_4am
    
    # 条件2: 上次重置日期不是今天
    condition2 = last_reset_date != today_date
    
    # 条件3: 上次签到时间早于今天4AM
    condition3 = last_check_in_dt < today_4am
    
    # 只有当所有条件都满足时才重置状态
    if condition1 and condition2 and condition3:
        check_in_data["lastResetDate"] = today_date.isoformat()
        check_in_data["canCheckIn"] = True
        user_data["user"]["checkIn"]["canCheckIn"] = 1
        for vs in user_data["user"]["activity"]["CHECKIN_VS"].values():
            if isinstance(vs, dict) and "canVote" in vs:
                vs["canVote"] = 1

        write_json(server_data, SERVER_DATA_PATH)
        write_json(user_data, USER_JSON_PATH)
    
    # 如果今天已经签到过，确保状态为False
    elif last_reset_date.date() == today_date:
        pass