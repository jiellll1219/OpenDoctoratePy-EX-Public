from flask import request

from constants import BATTLE_REPLAY_JSON_PATH
from utils import read_json, write_json


def campaignV2BattleStart():

    data = request.data
    request_data = request.get_json()
    data = {
        'battleId': 'abcdefgh-1234-5678-a1b2c3d4e5f6',
        'playerDataDelta': {
            'modified': {},
            'deleted': {}
        },
        'result': 0
    }

    replay_data = read_json(BATTLE_REPLAY_JSON_PATH)
    replay_data["current"] = request_data["stageId"]
    write_json(replay_data, BATTLE_REPLAY_JSON_PATH)

    return data


def campaignV2BattleFinish():

    data = request.data
    data = {
        "result": 0,
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data


def campaignV2BattleSweep():

    data = request.data
    data = {
        "result": 0,
        "apFailReturn": 1,
        "rewards": [],
        "unlockStages": [],
        "unusualRewards": [],
        "additionalRewards": [],
        "furnitureRewards": [],
        "diamondMaterialRewards": [
            {
                "type": "DIAMOND_SHD",
                "id": "4003",
                "count": 1
            }
        ],
        "currentFeeBefore": 0,
        "currentFeeAfter": 1,
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data

