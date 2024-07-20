from flask import request
from constants import TEMPLATEGOODLIST_PATH
from utils import read_json, write_json

def getGoodList():

    request_data = read_json(TEMPLATEGOODLIST_PATH, encoding="utf-8")

    return request_data

def buyGood():
    
    json_body = request.get_json

    return json_body