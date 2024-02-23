import os
import socket
import hashlib
import requests

from datetime import datetime
from flask import Response, stream_with_context, redirect, send_file, send_from_directory
from constants import CONFIG_PATH
from core.function.loadMods import loadMods
from utils import read_json, write_json

from threading import Thread, Event, Lock

header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"}
MODS_LIST = {
    "mods": [],
    "name": [],
    "path": [],
    "download": []
}


def writeLog(data):

    time = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    clientIp = socket.gethostbyname(socket.gethostname())
    print(f'{clientIp} - - [{time}] {data}')


def getFile(assetsHash, fileName):

    global MODS_LIST
    server_config = read_json(CONFIG_PATH)
    mode = server_config["server"]["mode"]
    version = server_config["version"]["android"]["resVersion"]
    basePath  = os.path.join('.', 'assets', version, 'redirect')
    
    if fileName == 'hot_update_list.json' and read_json(CONFIG_PATH)["assets"]["enableMods"]:
        MODS_LIST = loadMods()

    if not server_config["assets"]["downloadLocally"]:
        basePath  = os.path.join('.', 'assets', version)
        if fileName != 'hot_update_list.json'and fileName not in MODS_LIST["download"]:
            if mode == "cn":
                return redirect('https://ak.hycdn.cn/assetbundle/official/Android/assets/{}/{}'.format(version, fileName), 302)
            elif mode == "global":
                return redirect('https://ark-us-static-online.yo-star.com/assetbundle/official/Android/assets/{}/{}'.format(version, fileName), 302)

    if not os.path.isdir(basePath):
        os.makedirs(basePath)
    filePath = os.path.join(basePath, fileName)

    wrongSize = False
    if not os.path.basename(fileName) == 'hot_update_list.json':
        temp_hot_update_path = os.path.join(basePath, "hot_update_list.json")
        hot_update = read_json(temp_hot_update_path)
        if os.path.exists(filePath):
            for pack in hot_update["packInfos"]:
                if pack["name"] == fileName.rsplit(".", 1)[0]:
                    wrongSize = os.path.getsize(filePath) != pack["totalSize"]
                    break

    if server_config["assets"]["enableMods"] and fileName in MODS_LIST["download"]:
        for mod, path in zip(MODS_LIST["download"], MODS_LIST["path"]):
            if fileName == mod and os.path.exists(path):
                wrongSize = False
                filePath = path

    writeLog('/{}/{}'.format(version, fileName))

    if mode == "cn":
        return export('https://ak.hycdn.cn/assetbundle/official/Android/assets/{}/{}'.format(version, fileName), basePath, fileName, filePath, assetsHash, wrongSize)
    elif mode == "global":
        return export('https://ark-us-static-online.yo-star.com/assetbundle/official/Android/assets/{}/{}'.format(version, fileName), basePath, fileName, filePath, assetsHash, wrongSize)

downloading_files={}
downloading_files_lock=Lock()

def downloadFile(url, filePath):

    writeLog('\033[1;33mDownload {}\033[0;0m'.format(os.path.basename(filePath)))
    file = requests.get(url, headers=header, stream=True)

    with open(filePath, 'wb') as f:
        for chunk in file.iter_content(chunk_size=4096):
            f.write(chunk)



def export(url, basePath, fileName, filePath, assetsHash, redownload = False):

    server_config = read_json(CONFIG_PATH)

    if os.path.basename(filePath) == 'hot_update_list.json':
        
        if os.path.exists(filePath):
            hot_update_list = read_json(filePath)
        else:
            hot_update_list = requests.get(url, headers=header).json()
            write_json(hot_update_list, filePath)
            
        abInfoList = hot_update_list["abInfos"]
        newAbInfos = []
        
        for abInfo in abInfoList:
            if server_config["assets"]["enableMods"]:
                hot_update_list["versionId"] = assetsHash
                if len(abInfo["hash"]) == 24:
                    abInfo["hash"] = assetsHash
                if abInfo["name"] not in MODS_LIST["name"]:
                    newAbInfos.append(abInfo)
            else:
                newAbInfos.append(abInfo)

        if server_config["assets"]["enableMods"]:
            for mod in MODS_LIST["mods"]:
                newAbInfos.append(mod)

        hot_update_list["abInfos"] = newAbInfos

        cachePath = './assets/cache/'
        savePath = cachePath + 'hot_update_list.json'

        if not os.path.isdir(cachePath):
            os.makedirs(cachePath)
        write_json(hot_update_list, savePath)

        return send_file('../assets/cache/hot_update_list.json')

    downloading_files_lock.acquire()
    downloading_thread=None
    if filePath in downloading_files or not os.path.exists(filePath) or redownload:
        if filePath not in downloading_files:
            downloading_files[filePath]=Event()
            downloading_thread=Thread(target=downloadFile, args=(url, filePath))
            downloading_thread.start()
        event=downloading_files[filePath]
        downloading_files_lock.release()
        if downloading_thread is not None:
            downloading_thread.join()
            event.set()
            downloading_files_lock.acquire()
            del downloading_files[filePath]
            downloading_files_lock.release()
        else:
            event.wait()
    else:
        downloading_files_lock.release()
    return send_from_directory(os.path.join("..", basePath), fileName)
