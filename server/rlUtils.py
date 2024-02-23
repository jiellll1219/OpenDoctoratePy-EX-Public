from time import time
from random import choice, choices, random

from constants import RL_TABLE_URL, CHARACTER_TABLE_URL, USER_JSON_PATH, \
                    RLV2_TEMPBUFF_JSON_PATH, RLV2_NODESINFO, RLV2_CONFIG_PATH
from utils import read_json
from core.function.update import updateData

RL_TABLE = updateData(RL_TABLE_URL)
CHARACTER_TABLE = updateData(CHARACTER_TABLE_URL)

POPULATION_RECRUIT_MAP = {
    "0": 0,
    "1": 0,
    "2": 0,
    "3": 2,
    "4": 3,
    "5": 6,
}

POPULATION_UPGRADE_MAP = {
    "0": 0,
    "1": 0,
    "2": 0,
    "3": 1,
    "4": 2,
    "5": 3,
}

NODE_TYPE_MAP = {
    "Normal": 1,
    "Emergency": 2,
    "Trader": 8,
    "Rest": 16,
    "Encounter": 32,
    "Boon": 64,
    "Entertainment": 128
}

def process_buff(rl_data: dict, buff_data: dict):

    if buff_data["relic"]:
        rl_data = process_relic(rl_data, buff_data["items"])

    else:
        rl_data = update_property(rl_data, buff_data["items"])

    return rl_data

def process_relic(rl_data: dict, relics: list):

    relic_dict = RL_TABLE["details"]["rogue_1"]["relics"]

    for relic_item in relics:
        
        relic_count = "r_0"
        if rl_data["current"]["inventory"]["relic"].keys():
            relic_count = "r_" + str(int(list(rl_data["current"]["inventory"]["relic"].keys())[-1].split("r_")[1]) + 1)

        relic_buffs = relic_dict[relic_item["id"]]["buffs"]
        for relic_buff in relic_buffs:

            if relic_buff["key"] == "immediate_reward":
                relic_data = { "id": None, "count": 0 }
                for relic_blackboard in relic_buff["blackboard"]:
                    if relic_blackboard["key"] == "id": relic_data.update({"id": relic_blackboard["valueStr"]})
                    elif relic_blackboard["key"] == "count": relic_data.update({"count": relic_blackboard["value"]})
                
                rl_data = update_property(rl_data, [relic_data])

            elif relic_buff["key"] == "level_life_point_add":
                relic_data = { "id": "level_life_point_add", "count": relic_buff["blackboard"][0]["value"] }
                rl_data = update_property(rl_data, [relic_data])

            elif relic_buff["key"] == "item_cover_set":
                relic_data = { "id": None, "count": 0 }
                for relic_blackboard in relic_buff["blackboard"]:
                    if relic_blackboard["key"] == "id": relic_data.update({"id": relic_blackboard["valueStr"]})
                    elif relic_blackboard["key"] == "count": relic_data.update({"count": relic_blackboard["value"]})
                    
                if relic_data["id"] == "rogue_1_hp":
                    rl_data["current"]["player"]["property"]["hp"] = relic_data["count"]

        rl_data["current"]["inventory"]["relic"].update({
            relic_count: {
                "index": relic_count,
                "id": relic_item["id"],
                "count": 1,
                "ts": int(time())
            }
        })

    return rl_data

def update_property(rl_data: dict, update_items: list):

    for update_data in update_items:
        if update_data["id"] == "rogue_1_hp":
            rl_data["current"]["player"]["property"]["hp"] += update_data["count"]
        
        elif update_data["id"] == "rogue_1_population":
            rl_data["current"]["player"]["property"]["population"]["max"] += update_data["count"]

        elif update_data["id"] == "rogue_1_gold":
            rl_data["current"]["player"]["property"]["gold"] += update_data["count"]

        elif update_data["id"] == "rogue_1_squad_capacity":
            rl_data["current"]["player"]["property"]["capacity"] += update_data["count"]

        elif update_data["id"] == "level_life_point_add":
            rl_data["current"]["buff"]["tmpHP"] += update_data["count"]

    return rl_data


def update_recruit(rl_data: dict, recruit_dict: list):

    for recruit_ticket in recruit_dict:
        
        recruit_count = "t_0"
        if rl_data["current"]["inventory"]["recruit"].keys():
            keys = list(rl_data["current"]["inventory"]["recruit"].keys())
            recruit_count = "t_" + str(int(keys[-1].split("t_")[1]) + 1)

        rl_data["current"]["inventory"]["recruit"].update({
            recruit_count: {
                "index": recruit_count,
                "id": recruit_ticket,
                "state": 0,
                "list": [],
                "result": None,
                "ts": int(time()),
                "from": "initial",
                "mustExtra": 0, 
                "needAssist": True
            }
        })

    rl_data["current"]["player"]["pending"][0]["content"]["initRecruit"]["tickets"] = list(rl_data["current"]["inventory"]["recruit"].keys())
    return rl_data

def generate_recruit_list(rl_data: dict, recruit_ticket_key: str):

    cnt = 0
    recruit_char_list = []
    recruited_dict = {}

    user_data = read_json(USER_JSON_PATH)["user"]["troop"]["chars"]
    rlv2_temp_buff = read_json(RLV2_TEMPBUFF_JSON_PATH)
    rl_recruit_data = rl_data["current"]["inventory"]["recruit"]

    for _, recruit_data in rl_recruit_data.items():
        if not recruit_data["result"]:
            continue

        if recruit_data["result"]["charId"] not in list(recruited_dict.keys()):
            recruited_dict.update({recruit_data["result"]["charId"]: 0})

        if recruit_data["result"]["evolvePhase"] > 1:
            recruited_dict[recruit_data["result"]["charId"]] += 2
        else:
            recruited_dict[recruit_data["result"]["charId"]] += 1
    
    recruit_ticket_details = RL_TABLE["details"]["rogue_1"]["recruitTickets"][recruit_ticket_key]
    free_char_indexes = []

    for characterKey in CHARACTER_TABLE:
        if "char" not in characterKey:
            continue

        character = CHARACTER_TABLE[characterKey]

        if not (
            character["profession"] in recruit_ticket_details["professionList"] and 
            character["rarity"] in recruit_ticket_details["rarityList"]
        ) and not characterKey in recruit_ticket_details["extraCharIds"]:
            continue

        userChar = None
        for userCharNum in user_data:
            if user_data[userCharNum]["charId"] == characterKey:
                userChar = user_data[userCharNum]
                break

        if character["profession"] in rlv2_temp_buff["autoUpgrade"]:

            recruit_char = {
                "instId": cnt,
                "charId": userChar["charId"],
                "type": "NORMAL",
                "favorPoint": userChar["favorPoint"],
                "potentialRank": userChar["potentialRank"],
                "mainSkillLvl": userChar["mainSkillLvl"],
                "skin": userChar["skin"],
                "level": userChar["level"],
                "exp": userChar["exp"],
                "evolvePhase": userChar["evolvePhase"],
                "defaultSkillIndex": 0,
                "skills": userChar["skills"],
                "currentEquip": userChar["currentEquip"],
                "equip": userChar["equip"],
                "upgradeLimited": False,
                "upgradePhase": 1 if character["rarity"] > 1 else 0,
                "isUpgrade": False,
                "population": POPULATION_RECRUIT_MAP[str(character["rarity"])]
            }

        else:
    
            # Set max to E1 Max Lvl
            if userChar["skin"] == userChar["charId"] + "#2":
                userChar["skin"] = userChar["charId"] + "#1"

            maxEvolvePhase = len(character["phases"]) - 1
            evolvePhase = 1 if maxEvolvePhase > 0 else 0
            if evolvePhase > userChar["evolvePhase"]:
                evolvePhase = userChar["evolvePhase"]
            
            level = character["phases"][evolvePhase]["maxLevel"]
            if character["phases"][evolvePhase]["maxLevel"] > userChar["level"]:
                level = userChar["level"]

            if len(userChar["skills"]) == 3:
                userChar["skills"][-1]["unlock"] = 0

            recruit_char = {
                "instId": cnt,
                "charId": userChar["charId"],
                "type": "NORMAL",
                "favorPoint": userChar["favorPoint"],
                "potentialRank": userChar["potentialRank"],
                "mainSkillLvl": userChar["mainSkillLvl"],
                "skin": userChar["skin"],
                "level": level,
                "exp": userChar["exp"],
                "evolvePhase": evolvePhase,
                "defaultSkillIndex": 0,
                "skills": userChar["skills"],
                "currentEquip": None,
                "equip": userChar["equip"],
                "upgradeLimited": True,
                "upgradePhase": 0,
                "isUpgrade": False,
                "population": POPULATION_RECRUIT_MAP[str(character["rarity"])]
            }

            recruited_unit = None
            if maxEvolvePhase == 2 and characterKey in list(recruited_dict.keys()) and recruited_dict[characterKey] % 2 == 1:
                for _, recruit_data in rl_recruit_data.items():
                    if not recruit_data["result"]:
                        continue
                    
                    if recruit_data["result"]["charId"] != characterKey:
                        continue

                    if recruit_data["result"]["evolvePhase"] == 1:
                        continue

                    recruited_unit = recruit_data["result"]
                    break

            if recruited_unit:
                recruit_char["type"] = recruit_data["type"]
                recruit_char["skin"] = recruit_char["charId"] + "#2"

                recruit_char["evolvePhase"] = userChar["evolvePhase"]
                recruit_char["level"] = userChar["level"]

                if len(recruit_char["skills"]) == 3: recruit_char["skills"][-1]["unlock"] = 1
                recruit_char["currentEquip"] = list(recruit_char["equip"].keys())[-1]
                recruit_char["upgradeLimited"] = False
                recruit_char["upgradePhase"] = 1
                recruit_char["isUpgrade"] = True
                recruit_char["population"] = POPULATION_UPGRADE_MAP[str(character["rarity"])]

        if character["rarity"] in recruit_ticket_details["extraFreeRarity"]:
            free_char_indexes.append(cnt)

        recruit_char_list.append(recruit_char)
        cnt += 1

    if free_char_indexes:
        free_char_index = choice(free_char_indexes)

        recruit_char_list[free_char_index]["type"] = "FREE"
        if recruit_char_list[free_char_index]["evolvePhase"] < 2:
            recruit_char_list[free_char_index]["population"] = 0

    return recruit_char_list

def generate_zone_map(zone: int):

    node_details = read_json(RLV2_NODESINFO)
    zone_setting = read_json(RLV2_CONFIG_PATH)["zoneSettings"]
    zone_detail = {}
    for x_index in range(zone_setting["zones"][f"zone_" + str(zone)]["x_count"]):
        for y_index in range(zone_setting["zones"][f"zone_" + str(zone)]["y_count"]):

            if y_index > 3:
                break

            weights = [zone_setting["chances"][node_weight_key] for node_weight_key in list(zone_setting["chances"].keys())]
            node_type = choices(list(zone_setting["chances"].keys()), k=1, weights=weights)[0]

            if x_index == 0:
                node_index = ""
            else:
                node_index = f"{x_index}0"

            node_index += str(y_index)
            node = {
                "index": node_index,
                "pos": {
                    "x": x_index,
                    "y": y_index
                },
                "next": [],
                "type": NODE_TYPE_MAP[node_type]
            }

            for y_sub_index in range(zone_setting["zones"][f"zone_" + str(zone)]["y_count"]):
                
                if y_sub_index > 3:
                    break

                if x_index == zone_setting["zones"][f"zone_" + str(zone)]["x_count"] - 1:
                    break

                node["next"].append({ 
                    "x": x_index+1,
                    "y": y_sub_index
                })

            if node_type in ["Normal", "Emergency"]:
                node.update({"stage": choices(node_details["BattleZones"][str(zone)][node_type], k=1)[0]})

            if x_index == zone_setting["zones"][f"zone_" + str(zone)]["x_count"] - 1:
                node.update({"zone_end": True})

            zone_detail.update({node_index: node})
        
    return zone_detail
