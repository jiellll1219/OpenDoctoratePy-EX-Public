from constants import CONFIG_PATH
from utils import read_json
from time import time as real_time


def time():
    config_data = read_json(CONFIG_PATH)
    virtualtime = config_data["userConfig"]["virtualtime"]
    if virtualtime < 0:
        return int(real_time())
    return int(real_time() % (24 * 60 * 60) + virtualtime)
