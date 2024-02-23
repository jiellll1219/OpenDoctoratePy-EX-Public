from time import time
from random import sample
from flask import request

from constants import TOWERDATA_PATH, TOWER_TABLE_URL, USER_JSON_PATH

from utils import read_json, write_json, decrypt_battle_data, writeLog
from core.function.update import updateData

# TODO:
# - 我的号打不太过困难模式，所以困难模式如果有什么问题的话，欢迎提出来


TOWER_TABLE = updateData(TOWER_TABLE_URL)

def currentCoords(stageid: str):
    tower = read_json(TOWERDATA_PATH)
    for index, layer in enumerate(tower["tower"]["current"]["layer"]):
        if layer["id"] == stageid:
            return index

def createRecruitList():
    tower = read_json(TOWERDATA_PATH)
    user_data = read_json(USER_JSON_PATH)
    candidate = []
    allCards = [str(user_data["user"]["troop"]["chars"][key]["instId"]) for key in user_data["user"]["troop"]["chars"]]
    usedCards = [str(tower["tower"]["current"]["cards"][key]["relation"]) for key in tower["tower"]["current"]["cards"]]
    pickedCards = sample([card for card in allCards if card not in usedCards], 5)
    for pickedCard in pickedCards:
        candidate.append({
            "groupId": user_data["user"]["troop"]["chars"][pickedCard]["charId"],
            "type": "CHAR",
            "cards": [{
                "instId": "0",
                "type": "CHAR",
                "charId": user_data["user"]["troop"]["chars"][pickedCard]["charId"],
                "relation": pickedCard,
                "evolvePhase": user_data["user"]["troop"]["chars"][pickedCard]["evolvePhase"],
                "level": user_data["user"]["troop"]["chars"][pickedCard]["level"],
                "favorPoint": user_data["user"]["troop"]["chars"][pickedCard]["favorPoint"],
                "potentialRank": user_data["user"]["troop"]["chars"][pickedCard]["potentialRank"],
                "mainSkillLvl": user_data["user"]["troop"]["chars"][pickedCard]["mainSkillLvl"],
                "skills": user_data["user"]["troop"]["chars"][pickedCard]["skills"],
                "defaultSkillIndex": user_data["user"]["troop"]["chars"][pickedCard]["defaultSkillIndex"],
                "currentEquip": user_data["user"]["troop"]["chars"][pickedCard]["currentEquip"],
                "equip": user_data["user"]["troop"]["chars"][pickedCard]["equip"],
                "skin": user_data["user"]["troop"]["chars"][pickedCard]["skin"]
            }]
        })
    tower["tower"]["current"]["halftime"]["candidate"] = candidate
    write_json(tower, TOWERDATA_PATH)


def towerCreateGame():

    data = request.data
    request_data = request.get_json()
    
    if request_data["isHard"] == 1:
        levels = TOWER_TABLE["towers"][request_data["tower"]]["hardLevels"]
        mode = True
    else:
        levels = TOWER_TABLE["towers"][request_data["tower"]]["levels"]
        mode = False
    layer = []
    for level in levels:
        layer.append({
            "id": level,
            "try": 0,
            "pass": False,
        })

    tower = {
        "tower": {
            "current": {
                "cards": {},
                "godCard": {
                    "id": "",
                    "subGodCardId": "",
                },
                "halftime": {
                    "canGiveUp": False,
                    "candidate": [],
                    "count": 0,
                },
                "layer": layer,
                "reward": {
                    "high": 0,
                    "low": 0,
                },
                "status": {
                    "coord": 0,
                    "isHard": mode,
                    "start": round(time()),
                    "state": "INIT_GOD_CARD",
                    "strategy": "OPTIMIZE", #TODO: 策略系统（优选，自由）
                    "tactical": {
                        "CASTER": "",
                        "MEDIC": "",
                        "PIONEER": "",
                        "SNIPER": "",
                        "SPECIAL": "",
                        "SUPPORT": "",
                        "TANK": "",
                        "WARRIOR": ""
                    },
                    "tower": request_data["tower"],
                },
                "trap": []
            }
        },
        "currentStage": "",
    }
    write_json(tower, TOWERDATA_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "tower": read_json(TOWERDATA_PATH)["tower"]
            },
            "deleted": {}
        }
    }

    return data

def towerInitGodCard():

    data = request.data
    request_data = request.get_json()
    tower = read_json(TOWERDATA_PATH)

    tower["tower"]["current"]["status"]["state"] = "INIT_BUFF"
    tower["tower"]["current"]["godCard"]["id"] = request_data["godCardId"]
    write_json(tower, TOWERDATA_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "tower": read_json(TOWERDATA_PATH)["tower"]
            },
            "deleted": {}
        }
    }

    return data

def towerInitGame():

    data = request.data
    request_data = request.get_json()
    tower = read_json(TOWERDATA_PATH)

    tower["tower"]["current"]["status"]["state"] = "INIT_CARD"
    tower["tower"]["current"]["status"]["strategy"] = request_data["strategy"]
    tower["tower"]["current"]["status"]["tactical"] = request_data["tactical"]
    write_json(tower, TOWERDATA_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "tower": read_json(TOWERDATA_PATH)["tower"]
            },
            "deleted": {}
        }
    }

    return data

def towerInitCard():

    data = request.data
    request_data = request.get_json()
    tower = read_json(TOWERDATA_PATH)
    user_data = read_json(USER_JSON_PATH)

    tower["tower"]["current"]["status"]["state"] = "STANDBY"
    
    cnt = 1
    for slot in request_data["slots"]:
        tower["tower"]["current"]["cards"][str(cnt)] = {
            "charId": user_data["user"]["troop"]["chars"][str(slot["charInstId"])]["charId"],
            "currentEquip": slot["currentEquip"],
            "defaultEquip": slot["skillIndex"],
            "equip": user_data["user"]["troop"]["chars"][str(slot["charInstId"])]["equip"],
            "evolvePhase": user_data["user"]["troop"]["chars"][str(slot["charInstId"])]["evolvePhase"],
            "favorPoint": user_data["user"]["troop"]["chars"][str(slot["charInstId"])]["favorPoint"],
            "instId": str(cnt),
            "level": user_data["user"]["troop"]["chars"][str(slot["charInstId"])]["level"],
            "mainSkillLvl": user_data["user"]["troop"]["chars"][str(slot["charInstId"])]["mainSkillLvl"],
            "potentialRank": user_data["user"]["troop"]["chars"][str(slot["charInstId"])]["potentialRank"],
            "relation": str(slot["charInstId"]),
            "skills": user_data["user"]["troop"]["chars"][str(slot["charInstId"])]["skills"],
            "skin": user_data["user"]["troop"]["chars"][str(slot["charInstId"])]["skin"],
            "type": "CHAR"
        }
        cnt += 1

    write_json(tower, TOWERDATA_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "tower": read_json(TOWERDATA_PATH)["tower"]
            },
            "deleted": {}
        }
    }

    return data

def towerBattleStart():

    data = request.data
    request_data = request.get_json()
    tower = read_json(TOWERDATA_PATH)

    tower["tower"]["current"]["status"]["coord"] = currentCoords(request_data["stageId"])
    tower["currentStage"] = request_data["stageId"]
    for stage in tower["tower"]["current"]["layer"]:
        if stage["id"] == request_data["stageId"]:
            stage["try"] += 1
    write_json(tower, TOWERDATA_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "tower": read_json(TOWERDATA_PATH)["tower"]
            },
            "deleted": {}
        }
    }

    return data

def towerBattleFinish():

    data = request.data
    request_data = request.get_json()
    tower = read_json(TOWERDATA_PATH)
    BattleData = decrypt_battle_data(request_data["data"], 1672502400)
    trap = []
    writeLog("\033[1;31m" + str(BattleData) + "\033[0;0m")

    if BattleData["completeState"] == 1:
        tower["tower"]["current"]["layer"][tower["tower"]["current"]["status"]["coord"] - 1]["try"] += 1
        write_json(tower, TOWERDATA_PATH)

        data = {
            "drop": [],
            "isNewRecord": False,
            "trap": [],
            "playerDataDelta": {
                "modified": {},
                "deleted": {}
            }
        }
    else:
        if tower["currentStage"] == tower["tower"]["current"]["layer"][2]["id"]:
            tower["tower"]["current"]["status"]["state"] = "SUB_GOD_CARD_RECRUIT"
            for i in BattleData["battleData"]["stats"]["extraBattleInfo"]:
                if i.startswith("DETAILED") and i.endswith("legion_gain_reward_trap"):
                    trap.append({
                        "id": i.split(",")[1],
                        "alias": i.split(",")[2],
                    })
            tower["tower"]["current"]["trap"] = trap
        elif tower["currentStage"] == tower["tower"]["current"]["layer"][-1]["id"]:
            tower["tower"]["current"]["status"]["state"] = "END"
        else:
            tower["tower"]["current"]["status"]["state"] = "RECRUIT"
        
        for stage in tower["tower"]["current"]["layer"]:
            if stage["id"] == tower["currentStage"]:
                stage["try"] += 1

        tower["tower"]["current"]["status"]["coord"] += 1
        tower["tower"]["current"]["halftime"]["count"] += 1
        write_json(tower, TOWERDATA_PATH)
        createRecruitList()
        
        data = {
            "drop": [],
            "isNewRecord": False,
            "trap": trap,
            "playerDataDelta": {
                "modified": {
                    "tower": read_json(TOWERDATA_PATH)["tower"]
                },
                "deleted": {}
            }
        }


    return data

def towerRecruit():

    data = request.data
    request_data = request.get_json()
    tower = read_json(TOWERDATA_PATH)
    user_data = read_json(USER_JSON_PATH)

    if tower["tower"]["current"]["halftime"]["count"] == 1:
        tower["tower"]["current"]["status"]["state"] = "RECRUIT"
        tower["tower"]["current"]["halftime"]["count"] = 0
    else:
        tower["tower"]["current"]["status"]["state"] = "STANDBY"

    if request_data["giveUp"] == 1:
        pass
    else:
        cnt = len(tower["tower"]["current"]["cards"]) + 2
        charInstId = str(user_data["user"]["dexNav"]["character"][request_data["charId"]]["charInstId"])
        tower["tower"]["current"]["cards"][str(cnt)] = {
            "charId": request_data["charId"],
            "currentEquip": user_data["user"]["troop"]["chars"][charInstId]["currentEquip"],
            "defaultSkillIndex": user_data["user"]["troop"]["chars"][charInstId]["defaultSkillIndex"],
            "equip": user_data["user"]["troop"]["chars"][charInstId]["equip"],
            "evolvePhase": user_data["user"]["troop"]["chars"][charInstId]["evolvePhase"],
            "favorPoint": user_data["user"]["troop"]["chars"][charInstId]["favorPoint"],
            "instId": str(cnt),
            "level": user_data["user"]["troop"]["chars"][charInstId]["level"],
            "mainSkillLvl": user_data["user"]["troop"]["chars"][charInstId]["mainSkillLvl"],
            "potentialRank": user_data["user"]["troop"]["chars"][charInstId]["potentialRank"],
            "relation": charInstId,
            "skills": user_data["user"]["troop"]["chars"][charInstId]["skills"],
            "skin": user_data["user"]["troop"]["chars"][charInstId]["skin"],
            "type": "CHAR"
        }

    write_json(tower, TOWERDATA_PATH)
    createRecruitList()

    data = {
        "playerDataDelta": {
            "modified": {
                "tower": read_json(TOWERDATA_PATH)["tower"]
            },
            "deleted": {}
        }
    }

    return data

def towerChooseSubGodCard():

    data = request.data
    request_data = request.get_json()
    tower = read_json(TOWERDATA_PATH)

    tower["tower"]["current"]["status"]["state"] = "STANDBY"
    tower["tower"]["current"]["godCard"]["subGodCardId"] = request_data["subGodCardId"]
    write_json(tower, TOWERDATA_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "tower": read_json(TOWERDATA_PATH)["tower"]
            },
            "deleted": {}
        }
    }

    return data

def towerSettleGame():

    data = request.data
    request_data = request.get_json()
    tower = read_json(TOWERDATA_PATH)

    data = {
        "reward": {
            "high": {
                "cnt": 0,
                "from": 24,
                "to": 24
            },
            "low": {
                "cnt": 0,
                "from": 60,
                "to": 60
            }
        },
        "ts": round(time()),
        "playerDataDelta": {
            "modified": {
                "tower": {
                    "current": {
                        "status": {
                            "state": "NONE",
                            "tower": "",
                            "coord": 0,
                            "tactical": {
                                "PIONEER": "",
                                "WARRIOR": "",
                                "TANK": "",
                                "SNIPER": "",
                                "CASTER": "",
                                "SUPPORT": "",
                                "MEDIC": "",
                                "SPECIAL": ""
                            },
                            "startegy": "OPTIMIZE",
                            "start": 0,
                            "isHard": False
                        },
                        "layer": [],
                        "cards": {},
                        "godCard": {
                            "id": "",
                            "subGodCardId": "",
                        },
                        "halftime": {
                            "count": 0,
                            "candidate": [],
                            "canGiceUp": False
                        },
                        "trap": [],
                        "raward": {}
                    }
                }
            },
            "deleted": {
                "tower": {
                    "current": {
                        "cards": [str(key) for key in tower["tower"]["current"]["cards"]]
                    }
                }
            }
        }
    }
    return data