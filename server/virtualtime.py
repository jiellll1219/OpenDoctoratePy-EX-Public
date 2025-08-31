from constants import CONFIG_PATH
from utils import read_json
from time import time as real_time
from datetime import datetime

def time():
    config_data = read_json(CONFIG_PATH)
    virtual_time = config_data["server"]["virtualtime"]
    
    if isinstance(virtual_time, str):
        # 兼容的时间格式列表
        time_formats = [
            "%Y/%m/%d %H:%M:%S",
            "%d%m%Y %H:%M:%S",
            "%d-%m-%Y %H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y%m%d %H:%M:%S",
        ]
        
        for fmt in time_formats:
            try:
                dt = datetime.strptime(virtual_time, fmt)
                return int(dt.timestamp())
            except ValueError:
                continue
        
        # 如果所有格式都不匹配，返回真实时间戳（防刁民措施）
        return int(real_time())
    
    elif isinstance(virtual_time, int):
        if virtual_time < 0:
            return int(real_time())
        return int(virtual_time)
    
    # 如果 virtualtime 类型不是 str 或 int，返回真实时间戳（防刁民措施）
    return int(real_time())