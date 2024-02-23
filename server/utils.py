import json
import socket
import hashlib

from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from flask import request
from threading import Thread, Lock, Event

with open("config/multiUserConfig.json") as f:
    multiUserConfig = json.load(f)
multiUserEnabled = multiUserConfig["enabled"]

users = {}
users_lock = Lock()

def writeLog(data):

    time = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    clientIp = socket.gethostbyname(socket.gethostname())
    print(f'{clientIp} - - [{time}] {data}')


def get_uid():
    if multiUserEnabled:
        try:
            uid = request.headers.get("Uid")
            if uid is None:
                raise Exception
            return uid
        except Exception:
            return "Anonymous"
    return None

def release_uid(uid):
    users_lock.acquire()
    user = users[uid]
    users_lock.release()
    event = user["EVENT"]
    while True:
        flag = event.wait(60.0*60.0)
        if flag:
            event.clear()
        else:
            break
    users_lock.acquire()
    del users[uid]
    users_lock.release()

def get_user(uid):
    users_lock.acquire()
    if uid not in users:
        users[uid] = {
            "CONTENT": {},
            "EVENT": Event()
        }
        Thread(target=release_uid, args=(uid,)).start()
    else:
        users[uid]["EVENT"].set()
    user = users[uid]
    users_lock.release()
    return user

def read_json(filepath: str, **args) -> dict:
    uid = get_uid()
    if uid is not None and filepath.find("hot_update_list.json") == -1:
        user = get_user(uid)
        if filepath in user["CONTENT"]:
            return json.loads(user["CONTENT"][filepath])
    with open(filepath, **args) as f:
        return json.load(f)


def write_json(data: dict, filepath: str) -> None:
    uid = get_uid()
    if uid is not None and filepath.find("hot_update_list.json") == -1:
        user = get_user(uid)
        user["CONTENT"][filepath] = json.dumps(data, sort_keys=False)
    else:
        with open(filepath, 'w') as f:
            json.dump(data, f, sort_keys=False, indent=4)


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
        writeLog("\033[1;31m" + str(e) + "\033[0;0m")
        return None