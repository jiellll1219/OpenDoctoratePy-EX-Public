import json
import hashlib
import asyncio
import threading
import traceback
import sys
import os

from msgspec.json import Encoder, Decoder, format
from typing import Optional
from typing import Dict, Any
from datetime import datetime
from hashlib import sha3_512
from random import shuffle
from flask import after_this_request
from datetime import datetime, UTC
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from constants import USER_JSON_PATH, CONFIG_PATH

json_encoder = Encoder(order="deterministic")
json_decoder = Decoder(strict=False)

def read_json(path: str) -> Dict[str, Any]:
    with open(path, "rb") as f:
        return json_decoder.decode(f.read())

def write_json(data: Any, path: str, indent: int = 4):
    with open(path, "wb") as f:
        f.write(format(json_encoder.encode(data), indent=indent))

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

def logging(data):
    def rand_name(len: int = 16) -> str:
        dt = datetime.now()
        time = (dt.year, dt.month, dt.day)
        seed = ""
        for t in time:
            seed += str(t)
        seed = str(shuffle(list(seed)))
        return sha3_512(seed.encode()).hexdigest()[:len]
    name = rand_name(8)
    log_message = f"[{datetime.now(UTC).isoformat()}] {data}"
    print(log_message)
    with open(f"logs/{name}.log", "w") as f:
        f.write(log_message)

def run_after_response(func, *args, on_error=None):
    """
    在函数返回后异步执行函数（带线程池、异常捕获）。

    :param func: 要执行的函数。支持带一个参数(data)，亦可以无参数。
    :param *args: 可选，传给函数的参数/数据。
    :param on_error: 可选，异常回调函数。例子: on_error(exception, traceback_str)
    """
    @after_this_request
    def register(response):
        async def task():
            try:
                await asyncio.to_thread(func, *args)
            except Exception as e:
                tb_str = traceback.format_exc()
                if on_error:
                    on_error(e, tb_str)
                else:
                    print(f"[处理异常] {e}", file=sys.stderr)
                    print(tb_str, file=sys.stderr)

        asyncio.run_coroutine_threadsafe(task(), global_loop)
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
                memory_cache[key] = read_json(file_path)
            except Exception as e:
                print(f"加载 {filename} 时出错: {str(e)}")

global_loop: Optional[asyncio.AbstractEventLoop] = None
def start_global_event_loop() -> asyncio.AbstractEventLoop:
    global global_loop
    if global_loop is not None:
        return global_loop

    loop = asyncio.new_event_loop()

    def _run_loop():
        asyncio.set_event_loop(loop)
        loop.run_forever()

    t = threading.Thread(target=_run_loop, daemon=True)
    t.start()

    global_loop = loop
    return loop

def get_memory(key: str) -> dict:
    '''
    从内存缓存中获取数据

    :param key: 要获取的数据的名，如"activity_table"，返回"data/excel/activity_table.json"中的数据
    '''
    global memory_cache
    useMemoryCache = memory_cache["config"]["server"]["useMemoryCache"]
    if useMemoryCache or key == "config":
        # 从内存缓存中获取数据，如果不存在则尝试读取文件
        try:
            return memory_cache[key]
        except KeyError:
            print(f"警告: {key} 未在缓存中找到，正在尝试从文件中加载")
            file_path = f"data/excel/{key}.json"
            try:
                # 将加载的数据存入缓存以备后续使用
                data = read_json(file_path)
                memory_cache[key] = data
                return data
            except FileNotFoundError:
                raise KeyError(f"未找到文件: {file_path}")
            except Exception as e:
                raise ValueError(f"加载 {file_path} 时出错: {str(e)}")
    # 如果不使用内存缓存，则直接从文件中读取数据
    else:
        file_path = f"data/excel/{key}.json"
        try:
            return read_json(file_path)
        except FileNotFoundError:
            raise KeyError(f"未找到文件: {file_path}")
        except Exception as e:
            raise ValueError(f"加载 {file_path} 时出错: {str(e)}")

def load_config() -> None:
    global memory_cache
    memory_cache["config"] = read_json(CONFIG_PATH)
    