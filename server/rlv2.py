from flask import request
from copy import deepcopy
from virtualtime import time
import random
import json

from constants import (
    RLV2_JSON_PATH,
    RLV2_USER_SETTINGS_PATH,
    USER_JSON_PATH,
    RL_TABLE_PATH,
    CONFIG_PATH,
    RLV2_SETTINGS_PATH
)

from utils import read_json, write_json, decrypt_battle_data, get_memory


def rlv2GiveUpGame():
    return {
        "result": "ok",
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": {
                        "player": None,
                        "record": None,
                        "map": None,
                        "troop": None,
                        "inventory": None,
                        "game": None,
                        "buff": None,
                        "module": None,
                    }
                }
            },
            "deleted": {},
        },
    }


def getChars(use_user_defaults=False):
    user_data = read_json(USER_JSON_PATH)
    chars = [
        user_data["user"]["troop"]["chars"][i]
        for i in user_data["user"]["troop"]["chars"]
    ]
    if use_user_defaults:
        rlv2_user_settings = read_json(RLV2_USER_SETTINGS_PATH)
        initialChars = set(rlv2_user_settings["initialChars"])
        chars_tmp = []
        for char in chars:
            if char["charId"] in initialChars:
                chars_tmp.append(char)
        chars = chars_tmp
    for i in range(len(chars)):
        char = chars[i]
        if char["evolvePhase"] == 2:
            char_alt = deepcopy(char)
            char_alt["evolvePhase"] = 1
            char_alt["level"] -= 10
            if len(char_alt["skills"]) == 3:
                char_alt["defaultSkillIndex"] = 1
                char_alt["skills"][-1]["unlock"] = 0
            for skill in char_alt["skills"]:
                skill["specializeLevel"] = 0
            char_alt["currentEquip"] = None
            chars.append(char_alt)
            if char["charId"] == "char_002_amiya":
                tmpls = list(char_alt["tmpl"].keys())
                for j in tmpls:
                    if len(char_alt["tmpl"][j]["skills"]) == 3:
                        char_alt["tmpl"][j]["defaultSkillIndex"] = 1
                        char_alt["tmpl"][j]["skills"][-1]["unlock"] = 0
                    for skill in char_alt["tmpl"][j]["skills"]:
                        skill["specializeLevel"] = 0
                    char_alt["tmpl"][j]["currentEquip"] = None
                char["currentTmpl"] = tmpls[0]
                char_alt["currentTmpl"] = tmpls[0]
                for j in range(1, len(tmpls)):
                    for k in [char, char_alt]:
                        char_alt_alt = deepcopy(k)
                        char_alt_alt["currentTmpl"] = tmpls[j]
                        chars.append(char_alt_alt)
    for i, char in enumerate(chars):
        char.update(
            {
                "instId": str(i),
                "type": "NORMAL",
                "upgradeLimited": False,
                "upgradePhase": 1,
                "isUpgrade": False,
                "isCure": False,
                "population": 0,
                "charBuff": [],
                "troopInstId": "0",
            }
        )
        if char["evolvePhase"] < 2:
            char["upgradeLimited"] = True
            char["upgradePhase"] = 0
    return chars


def rlv2CreateGame():
    request_data = request.get_json()

    theme = request_data["theme"]
    mode = request_data["mode"]
    if mode == "MONTH_TEAM" or mode == "CHALLENGE":
        mode = "NORMAL"
    mode_grade = request_data["modeGrade"]

    match theme:
        case "rogue_1":
            bands = [
                "rogue_1_band_1",
                "rogue_1_band_2",
                "rogue_1_band_3",
                "rogue_1_band_4",
                "rogue_1_band_5",
                "rogue_1_band_6",
                "rogue_1_band_7",
                "rogue_1_band_8",
                "rogue_1_band_9",
                "rogue_1_band_10",
            ]
            ending = random.choice(["ro_ending_1", "ro_ending_2", "ro_ending_3", "ro_ending_4"])
        case "rogue_2":
            bands = [
                "rogue_2_band_1",
                "rogue_2_band_2",
                "rogue_2_band_3",
                "rogue_2_band_4",
                "rogue_2_band_5",
                "rogue_2_band_6",
                "rogue_2_band_7",
                "rogue_2_band_8",
                "rogue_2_band_9",
                "rogue_2_band_10",
                "rogue_2_band_11",
                "rogue_2_band_12",
                "rogue_2_band_13",
                "rogue_2_band_14",
                "rogue_2_band_15",
                "rogue_2_band_16",
                "rogue_2_band_17",
                "rogue_2_band_18",
                "rogue_2_band_19",
                "rogue_2_band_20",
                "rogue_2_band_21",
                "rogue_2_band_22",
            ]
            ending = random.choice(["ro2_ending_1", "ro2_ending_2", "ro2_ending_3", "ro2_ending_4"])
        case "rogue_3":
            bands = [
                "rogue_3_band_1",
                "rogue_3_band_2",
                "rogue_3_band_3",
                "rogue_3_band_4",
                "rogue_3_band_5",
                "rogue_3_band_6",
                "rogue_3_band_7",
                "rogue_3_band_8",
                "rogue_3_band_9",
                "rogue_3_band_10",
                "rogue_3_band_11",
                "rogue_3_band_12",
                "rogue_3_band_13",
            ]
            ending = random.choice(["ro3_ending_1", "ro3_ending_2", "ro3_ending_3", "ro3_ending_4"])
        case "rogue_4":
            bands = [
                "rogue_4_band_1",
                "rogue_4_band_2",
                "rogue_4_band_3",
                "rogue_4_band_4",
                "rogue_4_band_5",
                "rogue_4_band_6",
                "rogue_4_band_7",
                "rogue_4_band_8",
                "rogue_4_band_9",
                "rogue_4_band_10",
                "rogue_4_band_11",
                "rogue_4_band_12",
                "rogue_4_band_14",
                "rogue_4_band_15",
                "rogue_4_band_16",
                "rogue_4_band_17",
                "rogue_4_band_18",
                "rogue_4_band_19",
                "rogue_4_band_20",
                "rogue_4_band_21",
                "rogue_4_band_22",
            ]
            ending = random.choice(["ro4_ending_1", "ro4_ending_2", "ro4_ending_3", "ro4_ending_4"])
        case "rogue_5":
            bands = [
                "rogue_5_band_1",
                "rogue_5_band_2",
                "rogue_5_band_3",
                "rogue_5_band_4",
                "rogue_5_band_5",
                "rogue_5_band_6",
                "rogue_5_band_7",
                "rogue_5_band_8",
                "rogue_5_band_9",
                "rogue_5_band_10",
                "rogue_5_band_11",
                "rogue_5_band_12",
                "rogue_5_band_13",
                "rogue_5_band_14",
                "rogue_5_band_15",
                "rogue_5_band_16",
                "rogue_5_band_17",
                "rogue_5_band_18",
                "rogue_5_band_19",
                "rogue_5_band_20",
            ]
            ending = random.choice(["ro5_ending_1", "ro5_ending_2", "ro5_ending_3"])
        case _:
            bands = []
            ending = ""

    rlv2 = {
        "player": {
            "state": "INIT",
            "property": {
                "exp": 0,
                "level": 10,
                "maxLevel": 10,
                "hp": {"current": 10000, "max": 10000},
                "gold": 450,
                "shield": 10000,
                "capacity": 10000,
                "population": {"cost": 0, "max": 6},
                "conPerfectBattle": 0,
            },
            "cursor": {"zone": 0, "position": None},
            "trace": [],
            "pending": [
                {
                    "index": "e_0",
                    "type": "GAME_INIT_RELIC",
                    "content": {
                        "initRelic": {
                            "step": [1, 3],
                            "items": {
                                str(i): {"id": band, "count": 1}
                                for i, band in enumerate(bands)
                            },
                        }
                    },
                },
                {
                    "index": "e_1",
                    "type": "GAME_INIT_RECRUIT_SET",
                    "content": {
                        "initRecruitSet": {
                            "step": [2, 3],
                            "option": ["recruit_group_1"],
                        }
                    },
                },
                {
                    "index": "e_2",
                    "type": "GAME_INIT_RECRUIT",
                    "content": {
                        "initRecruit": {
                            "step": [3, 3],
                            "tickets": [],
                            "showChar": [],
                            "team": None,
                        }
                    },
                },
            ],
            "status": {"bankPut": 0},
            "toEnding": ending,
            "chgEnding": False,
        },
        "record": {"brief": None},
        "map": {"zones": {}},
        "troop": {
            "chars": {},
            "expedition": [],
            "expeditionReturn": None,
            "hasExpeditionReturn": False,
        },
        "inventory": {
            "relic": {},
            "recruit": {},
            "trap": None,
            "consumable": {},
            "exploreTool": {},
        },
        "game": {
            "mode": mode,
            "predefined": None,
            "theme": theme,
            "outer": {"support": False},
            "start": time(),
            "eGrade": mode_grade,
            "equivalentGrade": mode_grade,
        },
        "buff": {"tmpHP": 0, "capsule": None, "squadBuff": []},
        "module": {},
    }
    write_json(rlv2, RLV2_JSON_PATH)

    config = read_json(CONFIG_PATH)
    if config["rlv2Config"]["allChars"]:
        match theme:
            case "rogue_1":
                ticket = "rogue_1_recruit_ticket_all"
            case "rogue_2":
                ticket = "rogue_2_recruit_ticket_all"
            case "rogue_3":
                ticket = "rogue_3_recruit_ticket_all"
            case "rogue_4":
                ticket = "rogue_4_recruit_ticket_all"
            case "rogue_5":
                ticket = "rogue_5_recruit_ticket_all"
            case _:
                ticket = ""
        chars = getChars(use_user_defaults=True)
        for i, char in enumerate(chars):
            ticket_id = f"t_{i}"
            char_id = str(i + 1)
            char["instId"] = char_id
            rlv2["inventory"]["recruit"][ticket_id] = {
                "index": f"t_{i}",
                "id": ticket,
                "state": 2,
                "list": [],
                "result": char,
                "ts": time() - 300,
                "from": "initial",
                "mustExtra": 0,
                "needAssist": True,
            }
            rlv2["troop"]["chars"][char_id] = char

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def rlv2ChooseInitialRelic():
    request_data = request.get_json()
    select = request_data["select"]

    rlv2 = read_json(RLV2_JSON_PATH)
    band = rlv2["player"]["pending"][0]["content"]["initRelic"]["items"][select]["id"]
    rlv2["player"]["pending"].pop(0)
    rlv2["inventory"]["relic"]["r_0"] = {
        "index": "r_0",
        "id": band,
        "count": 1,
        "ts": time(),
    }
    write_json(rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def rlv2SelectChoice():
    rlv2 = read_json(RLV2_JSON_PATH)

    # write_json(rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def addTicket(rlv2, ticket_id):
    theme = rlv2["game"]["theme"]
    match theme:
        case "rogue_1":
            ticket = "rogue_1_recruit_ticket_all"
        case "rogue_2":
            ticket = "rogue_2_recruit_ticket_all"
        case "rogue_3":
            ticket = "rogue_3_recruit_ticket_all"
        case "rogue_4":
            ticket = "rogue_4_recruit_ticket_all"
        case "rogue_5":
            ticket = "rogue_5_recruit_ticket_all"
        case _:
            ticket = ""
    rlv2["inventory"]["recruit"][ticket_id] = {
        "index": ticket_id,
        "id": ticket,
        "state": 0,
        "list": [],
        "result": None,
        "ts": time(),
        "from": "initial",
        "mustExtra": 0,
        "needAssist": True,
    }


def getNextTicketIndex(rlv2):
    d = set()
    for e in rlv2["inventory"]["recruit"]:
        d.add(int(e[2:]))
    config = read_json(CONFIG_PATH)
    if not config["rlv2Config"]["allChars"]:
        i = 0
    else:
        i = 10000 - 1
    while i in d:
        i += 1
    return f"t_{i}"


def rlv2ChooseInitialRecruitSet():
    rlv2 = read_json(RLV2_JSON_PATH)
    rlv2["player"]["pending"].pop(0)

    config = read_json(CONFIG_PATH)
    if not config["rlv2Config"]["allChars"]:
        for i in range(3):
            ticket_id = getNextTicketIndex(rlv2)
            addTicket(rlv2, ticket_id)
            rlv2["player"]["pending"][0]["content"]["initRecruit"]["tickets"].append(
                ticket_id
            )

    write_json(rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def getNextPendingIndex(rlv2):
    d = set()
    for e in rlv2["player"]["pending"]:
        d.add(int(e["index"][2:]))
    i = 0
    while i in d:
        i += 1
    return f"e_{i}"


def activateTicket(rlv2, ticket_id):
    pending_index = getNextPendingIndex(rlv2)
    rlv2["player"]["pending"].insert(
        0,
        {
            "index": pending_index,
            "type": "RECRUIT",
            "content": {"recruit": {"ticket": ticket_id}},
        },
    )
    chars = getChars()
    rlv2["inventory"]["recruit"][ticket_id]["state"] = 1
    rlv2["inventory"]["recruit"][ticket_id]["list"] = chars


def rlv2ActiveRecruitTicket():
    request_data = request.get_json()
    ticket_id = request_data["id"]

    rlv2 = read_json(RLV2_JSON_PATH)
    activateTicket(rlv2, ticket_id)
    write_json(rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def getNextCharId(rlv2):
    config = read_json(CONFIG_PATH)
    if not config["rlv2Config"]["allChars"]:
        i = 1
    else:
        i = 10000
    while str(i) in rlv2["troop"]["chars"]:
        i += 1
    return str(i)


def rlv2RecruitChar():
    request_data = request.get_json()
    ticket_id = request_data["ticketIndex"]
    option_id = int(request_data["optionId"])

    rlv2 = read_json(RLV2_JSON_PATH)
    rlv2["player"]["pending"].pop(0)
    char_id = getNextCharId(rlv2)
    char = rlv2["inventory"]["recruit"][ticket_id]["list"][option_id]
    char["instId"] = char_id
    rlv2["inventory"]["recruit"][ticket_id]["state"] = 2
    rlv2["inventory"]["recruit"][ticket_id]["list"] = []
    rlv2["inventory"]["recruit"][ticket_id]["result"] = char
    rlv2["troop"]["chars"][char_id] = char
    write_json(rlv2, RLV2_JSON_PATH)

    data = {
        "chars": [char],
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        },
    }

    return data


def rlv2CloseRecruitTicket():
    request_data = request.get_json()
    ticket_id = request_data["id"]

    rlv2 = read_json(RLV2_JSON_PATH)
    rlv2["player"]["pending"].pop(0)
    rlv2["inventory"]["recruit"][ticket_id]["state"] = 2
    rlv2["inventory"]["recruit"][ticket_id]["list"] = []
    rlv2["inventory"]["recruit"][ticket_id]["result"] = None
    write_json(rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def getMap(theme):
    with open (RL_TABLE_PATH, encoding='utf-8') as a:
        rlv2_table = json.load(a)
    stages = [i for i in rlv2_table["details"][theme]["stages"]]
    match theme:
        case "rogue_1":
            shop = 8
        case "rogue_2":
            shop = 4096
        case "rogue_3":
            shop = 4096
        case "rogue_4":
            shop = 4096
        case "rogue_5":
            shop = 4096
        case _:
            shop = 0
    map = {}
    zone = 1
    j = 0
    while j < len(stages):
        zone_map = {"id": f"zone_{zone}", "index": zone, "nodes": {}, "variation": []}
        nodes_list = [
            {
                "index": "0",
                "pos": {"x": 0, "y": 0},
                "next": [{"x": 1, "y": 0}],
                "type": shop,
            },
            {"index": "100", "pos": {"x": 1, "y": 0}, "next": [], "type": shop},
        ]
        x_max = 9
        y_max = 3
        x = 1
        y = 1
        while j < len(stages):
            stage = stages[j]
            if y > y_max:
                if x + 1 == x_max:
                    break
                x += 1
                y = 0
            node_type = 1
            if rlv2_table["details"][theme]["stages"][stage]["isElite"]:
                node_type = 2
            elif rlv2_table["details"][theme]["stages"][stage]["isBoss"]:
                node_type = 4
            nodes_list.append(
                {
                    "index": f"{x}0{y}",
                    "pos": {"x": x, "y": y},
                    "next": [],
                    "type": node_type,
                    "stage": stage,
                }
            )
            nodes_list[0]["next"].append({"x": x, "y": y})
            y += 1
            j += 1
        x += 1
        nodes_list[0]["next"].append({"x": x, "y": 0})
        nodes_list.append(
            {
                "index": f"{x}00",
                "pos": {"x": x, "y": 0},
                "next": [],
                "type": shop,
                "zone_end": True,
            }
        )

        for node in nodes_list:
            zone_map["nodes"][node["index"]] = node
        map[str(zone)] = zone_map
        zone += 1
    return map


def rlv2FinishEvent():
    rlv2 = read_json(RLV2_JSON_PATH)
    rlv2["player"]["state"] = "WAIT_MOVE"
    rlv2["player"]["cursor"]["zone"] = 1
    rlv2["player"]["pending"] = []
    theme = rlv2["game"]["theme"]
    write_json(rlv2, RLV2_JSON_PATH)

    # too large, do not send it every time
    rlv2["map"]["zones"] = getMap(theme)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def getZone(stage_id):
    rlv2_settings = read_json(RLV2_SETTINGS_PATH)
    if stage_id in rlv2_settings["stageZone"]:
        return rlv2_settings["stageZone"][stage_id]
    if stage_id.find("_n_") != -1 or stage_id.find("_e_") != -1:
        try:
            return int(stage_id.split("_")[2])
        except Exception:
            pass
    return -1


def getBuffs(rlv2, stage_id):
    rlv2_table = get_memory("roguelike_topic_table")
    theme = rlv2["game"]["theme"]
    buffs = []

    if rlv2["inventory"]["trap"] is not None:
        item_id = rlv2["inventory"]["trap"]["id"]
        if item_id in rlv2_table["details"][theme]["relics"]:
            buffs += rlv2_table["details"][theme]["relics"][item_id]["buffs"]
    for i in rlv2["inventory"]["exploreTool"]:
        item_id = rlv2["inventory"]["exploreTool"][i]["id"]
        if item_id in rlv2_table["details"][theme]["relics"]:
            buffs += rlv2_table["details"][theme]["relics"][item_id]["buffs"]

    for i in rlv2["buff"]["squadBuff"]:
        if i in rlv2_table["details"][theme]["squadBuffData"]:
            buffs += rlv2_table["details"][theme]["squadBuffData"][i]["buffs"]

    mode_grade = rlv2["game"]["eGrade"]
    match theme:
        case "rogue_1":
            theme_buffs = []
        case "rogue_2":
            theme_buffs = [
                # 0
                ([], []),
                # 1
                (
                    [
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "rogue_2_ep_damage_scale"},
                                {"key": "ep_damage_scale", "value": 1.15},
                            ],
                        },
                    ],
                    [],
                ),
                # 2
                ([], []),
                # 3
                (
                    [
                        {
                            "key": "enemy_attribute_add",
                            "blackboard": [{"key": "magic_resistance", "value": 10}],
                        },
                    ],
                    [],
                ),
                # 4
                ([], []),
                # 5
                (
                    [
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_atk_down"},
                                {"key": "atk", "value": 1.15},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "BOSS",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_def_down"},
                                {"key": "def", "value": 1.15},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "BOSS",
                                },
                            ],
                        },
                    ],
                    [],
                ),
                # 6
                ([], []),
                # 7
                (
                    [
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_move_speed_down"},
                                {"key": "move_speed", "value": 1.15},
                            ],
                        },
                    ],
                    [],
                ),
                # 8
                (
                    [
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "rogue_2_ep_damage_scale"},
                                {"key": "ep_damage_scale", "value": 1.3},
                            ],
                        },
                    ],
                    [1],
                ),
                # 9
                (
                    [
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_attack_speed_down"},
                                {"key": "attack_speed", "value": 15},
                            ],
                        },
                    ],
                    [],
                ),
                # 10
                ([], []),
                # 11
                (
                    [
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_max_hp_down"},
                                {"key": "max_hp", "value": 1.2},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "ELITE|BOSS",
                                },
                            ],
                        },
                    ],
                    [],
                ),
                # 12
                (
                    [
                        {
                            "key": "enemy_attribute_add",
                            "blackboard": [{"key": "magic_resistance", "value": 20}],
                        },
                    ],
                    [3],
                ),
                # 13
                (
                    [
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "rogue_2_ep_damage_scale"},
                                {"key": "ep_damage_scale", "value": 1.45},
                            ],
                        },
                    ],
                    [8],
                ),
                # 14
                (
                    [
                        {
                            "key": "level_char_limit_add",
                            "blackboard": [{"key": "value", "value": -1}],
                        },
                    ],
                    [],
                ),
                # 15
                (
                    [
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_atk_down"},
                                {"key": "atk", "value": 1.2},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "ELITE|BOSS",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_def_down"},
                                {"key": "def", "value": 1.2},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "ELITE|BOSS",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_max_hp_down"},
                                {"key": "max_hp", "value": 1.2},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "ELITE|BOSS",
                                },
                            ],
                        },
                    ],
                    [],
                ),
            ]
        case "rogue_3":
            theme_buffs = [
                # 0
                ([], []),
                # 1
                ([], []),
                # 2
                ([], []),
                # 3
                ([], []),
                # 4
                (
                    [
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_atk_down"},
                                {"key": "atk", "value": 1.1},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "ELITE",
                                },
                            ],
                        },
                    ],
                    [],
                ),
                # 5
                (
                    [
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_atk_down"},
                                {"key": "atk", "value": 1.05},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "NORMAL",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_max_hp_down"},
                                {"key": "max_hp", "value": 1.05},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "NORMAL",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_atk_down"},
                                {"key": "atk", "value": 1.15},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "ELITE",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_max_hp_down"},
                                {"key": "max_hp", "value": 1.05},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "ELITE",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_atk_down"},
                                {"key": "atk", "value": 1.05},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "BOSS",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_max_hp_down"},
                                {"key": "max_hp", "value": 1.05},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "BOSS",
                                },
                            ],
                        },
                    ],
                    [4],
                ),
                # 6
                ([], []),
                # 7
                (
                    [
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_def_down"},
                                {"key": "def", "value": 1.1},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "NORMAL",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_def_down"},
                                {"key": "def", "value": 1.1},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "ELITE",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_def_down"},
                                {"key": "def", "value": 1.1},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "BOSS",
                                },
                            ],
                        },
                    ],
                    [],
                ),
                # 8
                (
                    [
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {
                                    "key": "key",
                                    "valueStr": "enemy_damage_resistance[inf]",
                                },
                                {"key": "damage_resistance", "value": 0.05},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "NORMAL",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {
                                    "key": "key",
                                    "valueStr": "enemy_damage_resistance[inf]",
                                },
                                {"key": "damage_resistance", "value": 0.05},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "ELITE",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {
                                    "key": "key",
                                    "valueStr": "enemy_damage_resistance[inf]",
                                },
                                {"key": "damage_resistance", "value": 0.05},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "BOSS",
                                },
                            ],
                        },
                    ],
                    [],
                ),
                # 9
                (
                    [
                        {
                            "key": "level_char_limit_add",
                            "blackboard": [{"key": "value", "value": -1}],
                        },
                    ],
                    [],
                ),
                # 10
                (
                    [
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_atk_down"},
                                {"key": "atk", "value": 1.15},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "NORMAL",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_max_hp_down"},
                                {"key": "max_hp", "value": 1.05},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "NORMAL",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_atk_down"},
                                {"key": "atk", "value": 1.25},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "ELITE",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_max_hp_down"},
                                {"key": "max_hp", "value": 1.05},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "ELITE",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_atk_down"},
                                {"key": "atk", "value": 1.15},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "BOSS",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_max_hp_down"},
                                {"key": "max_hp", "value": 1.05},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "BOSS",
                                },
                            ],
                        },
                    ],
                    [5],
                ),
                # 11
                (
                    [
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {
                                    "key": "key",
                                    "valueStr": "enemy_damage_resistance[inf]",
                                },
                                {"key": "damage_resistance", "value": 0.05},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "NORMAL",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {
                                    "key": "key",
                                    "valueStr": "enemy_damage_resistance[inf]",
                                },
                                {"key": "damage_resistance", "value": 0.05},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "ELITE",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {
                                    "key": "key",
                                    "valueStr": "enemy_damage_resistance[inf]",
                                },
                                {"key": "damage_resistance", "value": 0.1},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "BOSS",
                                },
                            ],
                        },
                    ],
                    [8],
                ),
                # 12
                ([], []),
                # 13
                (
                    [
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {
                                    "key": "key",
                                    "valueStr": "enemy_damage_resistance[inf]",
                                },
                                {"key": "damage_resistance", "value": 0.05},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "NORMAL",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {
                                    "key": "key",
                                    "valueStr": "enemy_damage_resistance[inf]",
                                },
                                {"key": "damage_resistance", "value": 0.1},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "ELITE",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {
                                    "key": "key",
                                    "valueStr": "enemy_damage_resistance[inf]",
                                },
                                {"key": "damage_resistance", "value": 0.15},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "BOSS",
                                },
                            ],
                        },
                    ],
                    [11],
                ),
                # 14
                (
                    [
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_atk_down"},
                                {"key": "atk", "value": 1.15},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "NORMAL",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_def_down"},
                                {"key": "def", "value": 1.15},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "NORMAL",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_max_hp_down"},
                                {"key": "max_hp", "value": 1.1},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "NORMAL",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_atk_down"},
                                {"key": "atk", "value": 1.25},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "ELITE",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_def_down"},
                                {"key": "def", "value": 1.15},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "ELITE",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_max_hp_down"},
                                {"key": "max_hp", "value": 1.1},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "ELITE",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_atk_down"},
                                {"key": "atk", "value": 1.15},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "BOSS",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_def_down"},
                                {"key": "def", "value": 1.15},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "BOSS",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_max_hp_down"},
                                {"key": "max_hp", "value": 1.1},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "BOSS",
                                },
                            ],
                        },
                    ],
                    [7, 10],
                ),
                # 15
                (
                    [
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_atk_down"},
                                {"key": "atk", "value": 1.25},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "NORMAL",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_def_down"},
                                {"key": "def", "value": 1.25},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "NORMAL",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_max_hp_down"},
                                {"key": "max_hp", "value": 1.2},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "NORMAL",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_atk_down"},
                                {"key": "atk", "value": 1.35},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "ELITE",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_def_down"},
                                {"key": "def", "value": 1.25},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "ELITE",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_max_hp_down"},
                                {"key": "max_hp", "value": 1.2},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "ELITE",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_atk_down"},
                                {"key": "atk", "value": 1.25},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "BOSS",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_def_down"},
                                {"key": "def", "value": 1.25},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "BOSS",
                                },
                            ],
                        },
                        {
                            "key": "global_buff_normal",
                            "blackboard": [
                                {"key": "key", "valueStr": "enemy_max_hp_down"},
                                {"key": "max_hp", "value": 1.2},
                                {
                                    "key": "selector.enemy_level_type",
                                    "valueStr": "BOSS",
                                },
                            ],
                        },
                    ],
                    [14],
                ),
            ]
        case "rogue_4":
            theme_buffs = []
        case _:
            theme_buffs = []
    for i in range(len(theme_buffs)):
        if mode_grade < i:
            break
        for j in theme_buffs[i][1]:
            theme_buffs[j] = ([], [])
    for i in range(len(theme_buffs)):
        if mode_grade < i:
            break
        buffs += theme_buffs[i][0]
    zone = getZone(stage_id)
    if theme == "rogue_1":
        pass
    elif theme == "rogue_2":
        if zone == -1:
            zone = 6
        if mode_grade > 0:
            value = 1 + 0.01 * mode_grade
            for i in range(zone):
                buffs += [
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {"key": "key", "valueStr": "enemy_atk_down"},
                            {"key": "atk", "value": value},
                        ],
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {"key": "key", "valueStr": "enemy_max_hp_down"},
                            {"key": "max_hp", "value": value},
                        ],
                    },
                ]
    elif theme == "rogue_3":
        if zone == -1:
            zone = 7
        if mode_grade > 4:
            value = 1 + 0.16 * (mode_grade - 4) / (15 - 4)
            for i in range(zone):
                buffs += [
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {"key": "key", "valueStr": "enemy_atk_down"},
                            {"key": "atk", "value": value},
                        ],
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {"key": "key", "valueStr": "enemy_max_hp_down"},
                            {"key": "max_hp", "value": value},
                        ],
                    },
                ]
    elif theme == "rogue_4":
        if zone == -1:
            zone = 7
        if mode_grade > 4:
            value = 1 + 0.16 * (mode_grade - 4) / (15 - 4)
            for i in range(zone):
                buffs += [
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {"key": "key", "valueStr": "enemy_atk_down"},
                            {"key": "atk", "value": value},
                        ],
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {"key": "key", "valueStr": "enemy_max_hp_down"},
                            {"key": "max_hp", "value": value},
                        ],
                    },
                ]
    return buffs


def rlv2MoveAndBattleStart():
    request_data = request.get_json()
    stage_id = request_data["stageId"]
    x = request_data["to"]["x"]
    y = request_data["to"]["y"]

    rlv2 = read_json(RLV2_JSON_PATH)
    rlv2["player"]["state"] = "PENDING"
    rlv2["player"]["cursor"]["position"] = {"x": x, "y": y}
    rlv2["player"]["trace"].append(rlv2["player"]["cursor"])
    pending_index = getNextPendingIndex(rlv2)
    buffs = getBuffs(rlv2, stage_id)
    theme = rlv2["game"]["theme"]
    match theme:
        case "rogue_1":
            box_info = {}
        case "rogue_2":
            box_info = {
                random.choice(
                    ["trap_065_normbox", "trap_066_rarebox", "trap_068_badbox"]
                ): 100
            }
        case "rogue_3":
            box_info = {
                random.choice(
                    ["trap_108_smbox", "trap_109_smrbox", "trap_110_smbbox"]
                ): 100
            }
        case "rogue_4":
            box_info = {
                random.choice(
                    ["trap_757_skzbox", "trap_758_skzmbx", "trap_759_skzwyx"]
                ): 100
            },
        case "rogue_5":
            box_info = {
                random.choice(
                    ["rogue_5_stash_recruit", "pool_recruit_1"]
                ): 100
            }
        case _:
            box_info = {}
    dice_roll = []
    if theme == "rogue_2":
        dice_upgrade_count = 0
        band = rlv2["inventory"]["relic"]["r_0"]["id"]
        if (
            band == "rogue_2_band_16"
            or band == "rogue_2_band_17"
            or band == "rogue_2_band_18"
        ):
            dice_upgrade_count += 1
        for i in rlv2["inventory"]["relic"]:
            if rlv2["inventory"]["relic"][i]["id"] == "rogue_2_relic_grace_63":
                dice_upgrade_count += 1
        if dice_upgrade_count == 0:
            dice_face_count = 6
            dice_id = "trap_067_dice"
        elif dice_upgrade_count == 1:
            dice_face_count = 8
            dice_id = "trap_088_dice2"
        else:
            dice_face_count = 12
            dice_id = "trap_089_dice3"
        dice_roll = [random.randint(1, dice_face_count) for i in range(100)]
        buffs.append(
            {
                "key": "misc_insert_token_card",
                "blackboard": [
                    {"key": "token_key", "value": 0, "valueStr": dice_id},
                    {"key": "level", "value": 1, "valueStr": None},
                    {"key": "skill", "value": 0, "valueStr": None},
                    {"key": "cnt", "value": 100, "valueStr": None},
                ],
            }
        )
    rlv2["player"]["pending"].insert(
        0,
        {
            "index": pending_index,
            "type": "BATTLE",
            "content": {
                "battle": {
                    "state": 1,
                    "chestCnt": 100,
                    "goldTrapCnt": 100,
                    "diceRoll": dice_roll,
                    "boxInfo": box_info,
                    "tmpChar": [],
                    "sanity": 0,
                    "unKeepBuff": buffs,
                }
            },
        },
    )
    write_json(rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def rlv2BattleFinish():
    request_data = request.get_json()
    battle_data = decrypt_battle_data(request_data["data"])

    rlv2 = read_json(RLV2_JSON_PATH)
    if battle_data["completeState"] != 1:
        rlv2["player"]["pending"].pop(0)
        theme = rlv2["game"]["theme"]
        match theme:
            case "rogue_1":
                ticket = "rogue_1_recruit_ticket_all"
            case "rogue_2":
                ticket = "rogue_2_recruit_ticket_all"
            case "rogue_3":
                ticket = "rogue_3_recruit_ticket_all"
            case "rogue4":
                ticket = "rogue_4_recruit_ticket_all"
            case _:
                ticket = ""
        pending_index = getNextPendingIndex(rlv2)
        rlv2["player"]["pending"].insert(
            0,
            {
                "index": pending_index,
                "type": "BATTLE_REWARD",
                "content": {
                    "battleReward": {
                        "earn": {
                            "damage": 0,
                            "hp": 0,
                            "shield": 0,
                            "exp": 0,
                            "populationMax": 0,
                            "squadCapacity": 0,
                            "maxHpUp": 0,
                        },
                        "rewards": [
                            {
                                "index": 0,
                                "items": [{"sub": 0, "id": ticket, "count": 1}],
                                "done": 0,
                            }
                        ],
                        "show": "1",
                    }
                },
            },
        )
    else:
        rlv2["player"]["state"] = "WAIT_MOVE"
        rlv2["player"]["pending"] = []
        rlv2["player"]["cursor"]["position"]["x"] = 0
        rlv2["player"]["cursor"]["position"]["y"] = 0
        rlv2["player"]["trace"].pop()
    write_json(rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def rlv2FinishBattleReward():
    rlv2 = read_json(RLV2_JSON_PATH)
    rlv2["player"]["state"] = "WAIT_MOVE"
    rlv2["player"]["pending"] = []
    rlv2["player"]["cursor"]["position"]["x"] = 0
    rlv2["player"]["cursor"]["position"]["y"] = 0
    rlv2["player"]["trace"].pop()
    write_json(rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def getGoods(theme):
    match theme:
        case "rogue_1":
            ticket = "rogue_1_recruit_ticket_all"
            price_id = "rogue_1_gold"
        case "rogue_2":
            ticket = "rogue_2_recruit_ticket_all"
            price_id = "rogue_2_gold"
        case "rogue_3":
            ticket = "rogue_3_recruit_ticket_all"
            price_id = "rogue_3_gold"
        case "rogue_4":
            ticket = "rogue_4_recruit_ticket_all"
            price_id = "rogue_4_gold"
        case "rogue_5":
            ticket = "rogue_5_recruit_ticket_all"
            price_id = "rogue_5_gold"
        case _:
            ticket = ""
            price_id = ""
    goods = [
        {
            "index": "0",
            "itemId": ticket,
            "count": 1,
            "priceId": price_id,
            "priceCount": 0,
            "origCost": 0,
            "displayPriceChg": False,
            "_retainDiscount": 1,
        }
    ]
    i = 1
    rlv2_table = read_json(RL_TABLE_PATH)
    for j in rlv2_table["details"][theme]["archiveComp"]["relic"]["relic"]:
        goods.append(
            {
                "index": str(i),
                "itemId": j,
                "count": 1,
                "priceId": price_id,
                "priceCount": 0,
                "origCost": 0,
                "displayPriceChg": False,
                "_retainDiscount": 1,
            }
        )
        i += 1
    for j in rlv2_table["details"][theme]["difficultyUpgradeRelicGroups"]:
        for k in rlv2_table["details"][theme]["difficultyUpgradeRelicGroups"][j][
            "relicData"
        ]:
            goods.append(
                {
                    "index": str(i),
                    "itemId": k["relicId"],
                    "count": 1,
                    "priceId": price_id,
                    "priceCount": 0,
                    "origCost": 0,
                    "displayPriceChg": False,
                    "_retainDiscount": 1,
                }
            )
            i += 1
    for j in rlv2_table["details"][theme]["archiveComp"]["trap"]["trap"]:
        goods.append(
            {
                "index": str(i),
                "itemId": j,
                "count": 1,
                "priceId": price_id,
                "priceCount": 0,
                "origCost": 0,
                "displayPriceChg": False,
                "_retainDiscount": 1,
            }
        )
        i += 1
    return goods


def rlv2MoveTo():
    request_data = request.get_json()
    x = request_data["to"]["x"]
    y = request_data["to"]["y"]

    rlv2 = read_json(RLV2_JSON_PATH)
    rlv2["player"]["state"] = "PENDING"
    rlv2["player"]["cursor"]["position"] = {"x": x, "y": y}
    theme = rlv2["game"]["theme"]
    goods = getGoods(theme)
    rlv2["player"]["trace"].append(rlv2["player"]["cursor"])
    pending_index = getNextPendingIndex(rlv2)
    rlv2["player"]["pending"].insert(
        0,
        {
            "index": pending_index,
            "type": "SHOP",
            "content": {
                "shop": {
                    "bank": {
                        "open": False,
                        "canPut": False,
                        "canWithdraw": False,
                        "withdraw": 0,
                        "cost": 1,
                    },
                    "id": "just_a_shop",
                    "goods": goods,
                    "_done": False,
                }
            },
        },
    )
    write_json(rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def getNextRelicIndex(rlv2):
    d = set()
    for e in rlv2["inventory"]["relic"]:
        d.add(int(e[2:]))
    i = 0
    while i in d:
        i += 1
    return f"r_{i}"


def getNextExploreToolIndex(rlv2):
    d = set()
    for e in rlv2["inventory"]["exploreTool"]:
        d.add(int(e[2:]))
    i = 0
    while i in d:
        i += 1
    return f"e_{i}"


def rlv2LeaveShop():
    rlv2 = read_json(RLV2_JSON_PATH)
    rlv2["player"]["state"] = "WAIT_MOVE"
    rlv2["player"]["pending"] = []
    if rlv2["player"]["cursor"]["position"]["x"] > 1:
        rlv2["player"]["cursor"]["zone"] += 1
        rlv2["player"]["cursor"]["position"] = None
    elif rlv2["player"]["cursor"]["position"]["x"] == 1:
        rlv2["player"]["cursor"]["position"]["x"] = 0
        rlv2["player"]["cursor"]["position"]["y"] = 0
        rlv2["player"]["trace"].pop()
    write_json(rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data

def rlv2BuyGoods():
    request_data = request.get_json()
    select = int(request_data["select"][0])

    rlv2 = read_json(RLV2_JSON_PATH)
    item_id = rlv2["player"]["pending"][0]["content"]["shop"]["goods"][select]["itemId"]
    if item_id.find("_recruit_ticket_") != -1:
        ticket_id = getNextTicketIndex(rlv2)
        addTicket(rlv2, ticket_id)
        activateTicket(rlv2, ticket_id)
    elif item_id.find("_relic_") != -1:
        relic_id = getNextRelicIndex(rlv2)
        rlv2["inventory"]["relic"][relic_id] = {
            "index": relic_id,
            "id": item_id,
            "count": 1,
            "ts": 1695000000,
        }
    elif item_id.find("_active_tool_") != -1:
        rlv2["inventory"]["trap"] = {
            "index": item_id,
            "id": item_id,
            "count": 1,
            "ts": 1695000000,
        }
    elif item_id.find("_explore_tool_") != -1:
        explore_tool_id = getNextExploreToolIndex(rlv2)
        rlv2["inventory"]["exploreTool"][explore_tool_id] = {
            "index": explore_tool_id,
            "id": item_id,
            "count": 1,
            "ts": 1695000000,
        }
    write_json(rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def rlv2shopAction():

    json_body = request.get_json()

    try:
        select = int (json_body["buy"][0])
        return rlv2BuyGoods(select)
    except (KeyError, IndexError):
        return rlv2LeaveShop()


def rlv2ChooseBattleReward():
    request_data = request.get_json()
    index = request_data["index"]

    rlv2 = read_json(RLV2_JSON_PATH)
    if index == 0:
        ticket_id = getNextTicketIndex(rlv2)
        addTicket(rlv2, ticket_id)
        activateTicket(rlv2, ticket_id)
    write_json(rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data

def rlv2CopperRedraw():

    rlv2_data = read_json(RLV2_JSON_PATH)

    bag = rlv2_data["module"]["copper"]["bag"]
    for key, value in bag.items():
        value["isDrawn"] = False

    # a1 = random.sample(0, len(bag.keys()))
    copper = []
    L1 = random.sample(range(0, len(bag.keys())), 3)
    for key in L1:
        key = "c_" + str(key)
        copper.append(key)
        bag[key]["isDrawn"] = True

    write_json(rlv2_data, RLV2_JSON_PATH)

    data = {
        "copper": copper,
        "divineEventId": "rogue_5_levelEVE_2",
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": {
                        "module": {
                            "copper": {
                                "bag": bag,
                            }
                        }
                    }
                }
            },
            "deleted": {},
        }
    }

    return data