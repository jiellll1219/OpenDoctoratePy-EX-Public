import json
import uuid
from base64 import b64encode
from copy import deepcopy
from datetime import datetime
from hashlib import md5
from os.path import exists

from flask import request

from constants import (
    USER_JSON_PATH,
    CONFIG_PATH,
    BATTLE_REPLAY_JSON_PATH,
    SYNC_DATA_TEMPLATE_PATH,
    CRISIS_V2_JSON_BASE_PATH,
    MAILLIST_PATH,
    SQUADS_PATH
)
from user import checkin
from utils import read_json, write_json, get_memory, run_after_response
from virtualtime import time


def accountLogin():
    try:
        uid = uuid.UUID(request.headers.get("Uid"))
    except Exception:
        uid = uuid.uuid4()

    data = request.data
    data = {
        "result": 0,
        "uid": str(uid),
        "secret": "yostar",
        "serviceLicenseVersion": 0
    }

    run_after_response(checkin.update_check_in_status)
    return data


def accountSyncData():
    a = datetime.now()
    if not exists(USER_JSON_PATH):
        write_json({}, USER_JSON_PATH)

    saved_data = read_json(USER_JSON_PATH)
    mail_data = read_json(MAILLIST_PATH)
    player_data = read_json(SYNC_DATA_TEMPLATE_PATH)
    config = read_json(CONFIG_PATH)

    # 从内存中获取table
    skin_table = get_memory("skin_table")
    character_table = get_memory("character_table")
    equip_table = get_memory("uniequip_table")
    display_meta_table = get_memory("display_meta_table")
    retro_table = get_memory("retro_table")
    charm_table = get_memory("charm_table")
    activity_table = get_memory("activity_table")
    charword_table = get_memory("charword_table")
    stage_table = get_memory("stage_table")
    story_table = get_memory("story_table")
    addon_table = get_memory("handbook_info_table")
    story_review_table = get_memory("story_review_table")
    story_review_meta_table = get_memory("story_review_meta_table")
    enemy_handbook_table = get_memory("enemy_handbook_table")
    medal_table = get_memory("medal_table")

    ts = time()
    cntInstId = 1
    myCharList = {}
    charGroup = {}

    # 默认界面配置
    default_char_rotation = {
        "current": "1",
        "preset": {
            "1": {
                "background": "bg_rhodes_day",
                "homeTheme": "tm_rhodes_day",
                "name": "未命名的配置",
                "profile": "char_171_bldsk@witch#1",
                "profileInst": "171",
                "slots": [
                    {
                        "charId": "char_171_bldsk",
                        "skinId": "char_171_bldsk@witch#1"
                    }
                ]
            }
        }
    }
    try:
        player_data["user"].get("charRotation")
    except Exception:
        player_data["user"]["charRotation"] = default_char_rotation
    saved_data["user"]["charRotation"] = player_data["user"]["charRotation"]

    target_current = player_data["user"]["charRotation"]["current"]
    use_profile = player_data["user"]["charRotation"]["preset"][target_current]["profile"]
    for slots in player_data["user"]["charRotation"]["preset"][target_current]["slots"]:
        if slots.get("skinId") == use_profile:
            player_data["user"]["status"]["secretary"] = slots.get("charId")
            break
    player_data["user"]["status"]["secretarySkinId"] = use_profile
    player_data["user"]["background"]["selected"] = \
        player_data["user"]["charRotation"]["preset"][target_current]["background"]

    # 处理时装数据
    character_skins = {}
    temp_skin_table = {}
    # 遍历角色时装table并添加时装id到characterSkins中
    for skin_id, skin_data in skin_table["charSkins"].items():
        if "@" not in skin_id:
            continue
        character_skins[skin_id] = 1
        temp_skin_table[skin_data["charId"]] = skin_id
    player_data["user"]["skin"]["characterSkins"] = character_skins

    # 处理干员数据
    edit_json = config["charConfig"]
    player_data_keys = set(player_data["user"]["troop"]["chars"].keys())

    # 阿米娅的特殊模板
    AMIYA_TEMPLATES = {
        "char_002_amiya": {
            "skills": ["skcom_magic_rage[3]", "skchr_amiya_2", "skchr_amiya_3"],
            "skin": "char_002_amiya@test#1",
            "default_index": 2
        },
        "char_1001_amiya2": {
            "skills": ["skchr_amiya2_1", "skchr_amiya2_2"],
            "skin": "char_1001_amiya2@casc#1",
            "default_index": 1
        },
        "char_1037_amiya3": {
            "skills": ["skchr_amiya3_1", "skchr_amiya3_2"],
            "skin": "char_1001_amiya2@casc#1",
            "default_index": 1
        }
    }

    # 从玩家数据中获取已有角色字典
    troop_chars:dict = player_data["user"]["troop"]["chars"]
    # 获取玩家数据中的所有键（实例ID）并转换为集合
    player_data_keys = set(troop_chars.keys())
    # 从角色表中获取所有以"char_"开头的角色ID，并转换为列表
    char_ids = [cid for cid in character_table.keys() if cid.startswith("char_")]
    # 创建角色ID到实例ID的映射字典
    char_to_inst = {cid: str(int(cid.split("_")[1])) for cid in char_ids}
    # 创建实例ID到角色ID的反向映射字典
    inst_to_char = {inst: cid for cid, inst in char_to_inst.items()}

    # 获取所有候选实例ID的集合
    candidate_inst_ids = set(char_to_inst.values())
    # 找出玩家数据中已存在的实例ID
    existing = candidate_inst_ids & player_data_keys
    # 遍历已存在的实例ID，将角色数据添加到myCharList中
    for inst in existing:
        myCharList[inst] = troop_chars[inst]

    # 找出缺失的实例ID
    missing = candidate_inst_ids - existing
    # 遍历缺失的实例ID，从角色表中获取对应角色数据
    for inst in missing:
        char_id = inst_to_char[inst]
        char_data = character_table[char_id]
        inst_id = int(char_id.split("_")[1])

        # 新建干员
        voice_lan = charword_table["charDefaultTypeDict"].get(char_id, "JP")
        evolve_phase = edit_json["evolvePhase"]
        max_phase = len(char_data["phases"]) - 1
        evolve_phase = min(evolve_phase, max_phase) if evolve_phase != -1 else max_phase

        level = (
            edit_json["level"]
            if edit_json["level"] != -1
            else char_data["phases"][evolve_phase]["maxLevel"]
        )

        # 皮肤处理
        skin = temp_skin_table.get(char_id)
        if skin is None:
            skin = f"{char_id}#2" if evolve_phase >= 2 and char_data["displayNumber"] else f"{char_id}#1"

        operator = {
            "instId": inst_id,
            "charId": char_id,
            "favorPoint": edit_json["favorPoint"],
            "potentialRank": edit_json["potentialRank"],
            "mainSkillLvl": edit_json["mainSkillLvl"],
            "skin": skin,
            "level": level,
            "exp": 0,
            "evolvePhase": evolve_phase,
            "defaultSkillIndex": len(char_data["skills"]) - 1,
            "gainTime": ts,
            "skills": [],
            "voiceLan": voice_lan,
            "currentEquip": None,
            "equip": {},
            "starMark": 0,
        }

        # 技能处理
        for skill in char_data["skills"]:
            operator["skills"].append({
                "skillId": skill["skillId"],
                "unlock": 1,
                "state": 0,
                "specializeLevel": (
                    edit_json["skillsSpecializeLevel"]
                    if skill["levelUpCostCond"] and evolve_phase >= 2
                    else 0
                ),
                "completeUpgradeTime": -1
            })

        # 模组处理
        equip_list = equip_table["charEquip"].get(char_id)
        equip_dict = equip_table["equipDict"]
        if equip_list:
            operator["equip"] = {
                equip: {
                    "hide": 0,
                    "locked": 0,
                    "level": (
                        len(equip_dict[equip]["itemCost"])
                        if equip_dict[equip].get("itemCost") else 1
                    )
                } for equip in equip_list
            }
            operator["currentEquip"] = equip_list[-1]

        # 自定义配置覆盖
        if custom_data := edit_json["customUnitInfo"].get(char_id):
            for key, value in custom_data.items():
                if key == "skills":
                    for idx, sl in enumerate(value):
                        operator["skills"][idx]["specializeLevel"] = sl
                else:
                    operator[key] = value

        # 阿米娅的特殊处理
        if char_id == "char_002_amiya":
            operator.update({
                "defaultSkillIndex": -1,
                "skills": [],
                "currentTmpl": "char_002_amiya",
                "tmpl": {
                    key: {
                        "skinId": val["skin"],
                        "defaultSkillIndex": val["default_index"],
                        "skills": [{
                            "skillId": skill,
                            "unlock": 1,
                            "state": 0,
                            "specializeLevel": edit_json["skillsSpecializeLevel"],
                            "completeUpgradeTime": -1
                        } for skill in val["skills"]],
                        "currentEquip": None,
                        "equip": {}
                    } for key, val in AMIYA_TEMPLATES.items()
                }
            })
            for tmpl in AMIYA_TEMPLATES.keys():
                equip_list = equip_table["charEquip"].get(tmpl)
                operator["tmpl"][tmpl]["equip"] = {
                    equip: {
                        "hide": 0,
                        "locked": 0,
                        "level": (
                            len(equip_dict[equip]["itemCost"])
                            if equip_dict[equip].get("itemCost") else 1
                        )
                    } for equip in equip_list
                }
                operator["tmpl"][tmpl]["currentEquip"] = equip_list[-1]

        # 保存干员数据
        myCharList[str(inst_id)] = operator
        player_data["user"]["dexNav"]["character"][char_id] = {
            "charInstId": inst_id,
            "count": 6
        }

    cntInstId = 10000

    # 处理重复干员
    dupe_characters = edit_json["duplicateUnits"]
    char_id_index = {char["charId"]: inst_id for inst_id, char in myCharList.items()}
    for dupeCharId in dupe_characters:
        if (base_inst_id := char_id_index.get(dupeCharId)):
            tempChar = deepcopy(myCharList[str(base_inst_id)])
            tempChar["instId"] = cntInstId
            myCharList[str(cntInstId)] = tempChar
            cntInstId += 1

    # 更新角色信息
    player_data["user"]["troop"]["chars"] = myCharList
    player_data["user"]["troop"]["charGroup"] = charGroup
    player_data["user"]["troop"]["curCharInstId"] = cntInstId

    # Tamper story
    myStoryList = {"init": 1}
    for story in story_table:
        myStoryList.update({story: 1})

    player_data["user"]["status"]["flags"] = myStoryList

    # Tamper Stages
    myStageList = {}

    for stage in stage_table["stages"]:
        myStageList.update({
            stage: {
                "completeTimes": 1,
                "hasBattleReplay": 0,
                "noCostCnt": 0,
                "practiceTimes": 0,
                "stageId": stage_table["stages"][stage]["stageId"],
                "startTimes": 1,
                "state": 3
            }
        })

    player_data["user"]["dungeon"]["stages"] = myStageList

    # Tamper addon [paradox&records]
    addonList = {}
    for charId in addon_table["handbookDict"]:
        addonList[charId] = {"story": {}}
        story = addon_table["handbookDict"][charId]["handbookAvgList"]
        for i, j in zip(story, range(len(story))):
            if "storySetId" in i:
                addonList[charId]["story"].update({
                    addon_table["handbookDict"][charId]["handbookAvgList"][j]["storySetId"]: {
                        "fts": 1649232340,
                        "rts": 1649232340
                    }
                })

    for stage in addon_table["handbookStageData"]:
        addonList[stage].update({
            "stage": {
                addon_table["handbookStageData"][stage]["stageId"]: {
                    "startTimes": 0,
                    "completeTimes": 1,
                    "state": 3,
                    "fts": 1624284657,
                    "rts": 1624284657,
                    "startTime": 2
                }
            }
        })

    player_data["user"]["troop"]["addon"].update(addonList)  # TODO: I might try MongoDB in the future.

    # Tamper Side Stories and Intermezzis
    block = {}
    for retro in retro_table["retroActList"]:
        block.update({
            retro: {
                "locked": 0,
                "open": 1
            }
        })
    player_data["user"]["retro"]["block"] = block

    trail = {}
    for retro in retro_table["retroTrailList"]:
        trail.update({retro: {}})
        for trailReward in retro_table["retroTrailList"][retro]["trailRewardList"]:
            trail.update({
                retro: {
                    trailReward["trailRewardId"]: 1
                }
            })
    player_data["user"]["retro"]["trail"] = trail

    # Tamper Anniliations
    for stage in stage_table["stages"]:
        if stage.startswith("camp"):
            player_data["user"]["campaignsV2"]["instances"].update({
                stage: {
                    "maxKills": 400,
                    "rewardStatus": [1, 1, 1, 1, 1, 1, 1, 1]
                }
            })

            player_data["user"]["campaignsV2"]["sweepMaxKills"].update({stage: 400})
            player_data["user"]["campaignsV2"]["open"]["permanent"].append(stage)   #TODO 需要去重
            player_data["user"]["campaignsV2"]["open"]["training"].append(stage)

    # ------------------------------ 
    # 名片
    name_card_skin = player_data["user"]["nameCardStyle"]["skin"]["state"]
    skin_data = display_meta_table["nameCardV2Data"]["skinData"]
    for key in skin_data.keys():
        # 如果键不存在或者值为None，设置值为ture
        if key not in name_card_skin or name_card_skin[key] is None:
            name_card_skin[key] = {
                "progress": None,
                "unlock": True
            }
        else:
            pass

    # ------------------------------ 
    # 名片头像和背景
    avatar_icon = {}
    for avatar in display_meta_table["playerAvatarData"]["avatarList"]:
        avatar_icon.update({
            avatar["avatarId"]: {
                "ts": ts,
                "src": "initial" if avatar["avatarId"].startswith("avatar_def") else "other"
            }
        })
    player_data["user"]["avatar"]["avatar_icon"] = avatar_icon

    bgs = {}
    for bg in display_meta_table["homeBackgroundData"]["homeBgDataList"]:
        bgs.update({
            bg["bgId"]: {
                "unlock": ts
            }
        })
    player_data["user"]["background"]["bgs"] = bgs

    if "themeList" in display_meta_table["homeBackgroundData"]:
        themes = {}
        for theme in display_meta_table["homeBackgroundData"]["themeList"]:
            themes[theme["id"]] = {"unlock": 1691670000}
        player_data["user"]["homeTheme"]["themes"] = themes

    # ------------------------------ 
    # 更新charms
    for charm in charm_table["charmList"]:
        player_data["user"]["charm"]["charms"].update({charm["id"]: 1})

    # ------------------------------ 
    # 更新battle bus
    if "carData" in activity_table:
        for car_gear in activity_table["carData"]["carDict"]:
            player_data["user"]["car"]["accessories"].update({
                car_gear: {
                    "id": car_gear,
                    "num": len(activity_table["carData"]["carDict"][car_gear]["posList"])
                }
            })

    # Update Stultifera Navis
    deep_sea = player_data["user"]["deepSea"]
    activity_data = activity_table["activity"]["TYPE_ACT17SIDE"]["act17side"]
    deep_sea.update({
        "places": {place: 2 for place in activity_data["placeDataMap"]},
        "nodes": {node: 2 for node in activity_data["nodeInfoDataMap"]},
        "choices": {
            k: [2] * len(v["optionList"])
            for k, v in activity_data["choiceNodeDataMap"].items()
        }
    })

    for event in activity_data["eventDataMap"]:
        player_data["user"]["deepSea"]["events"].update({event: 1})

    for treasure in activity_data["treasureNodeDataMap"]:
        player_data["user"]["deepSea"]["treasures"].update({treasure: 1})

    for story in activity_data["storyNodeDataMap"]:
        player_data["user"]["deepSea"]["stories"].update(
            {activity_data["storyNodeDataMap"][story]["storyKey"]: 1}
        )

    for tech in activity_data["techTreeDataMap"]:
        player_data["user"]["deepSea"]["techTrees"].update({
            tech: {
                "state": 2,
                "branch": activity_data["techTreeDataMap"][tech]["defaultBranchId"]
            }
        })

    for log in activity_data["archiveItemUnlockDataMap"]:
        if not log.startswith("act17side_log_"):
            continue

        chapter = activity_data["archiveItemUnlockDataMap"][log]["chapterId"]
        if chapter in player_data["user"]["deepSea"]["logs"].keys():
            player_data["user"]["deepSea"]["logs"][chapter].append(log)
        else:
            player_data["user"]["deepSea"]["logs"].update({chapter: [log]})

    # Check if mail exists
    received_set = set(mail_data["recievedIDs"])
    deleted_set = set(mail_data["deletedIDs"])
    all_mails = set(mail_data["mailList"].keys())
    if not all_mails - (received_set | deleted_set):
        player_data["user"]["pushFlags"]["hasGifts"] = 1

    # Update timestamps
    current_ts = int(ts)
    ts_fields = [
        "lastRefreshTs", "lastApAddTime", "registerTs", "lastOnlineTs"
    ]
    for field in ts_fields:
        player_data["user"]["status"][field] = current_ts
    player_data["user"]["crisis"]["lst"] = ts
    player_data["user"]["crisis"]["nst"] = ts + 3600
    player_data["ts"] = ts

    replay_data = read_json(BATTLE_REPLAY_JSON_PATH)
    replay_data["currentCharConfig"] = md5(b64encode(json.dumps(edit_json).encode())).hexdigest()
    write_json(replay_data, BATTLE_REPLAY_JSON_PATH)

    # Enable battle replays
    if replay_data["currentCharConfig"] in list(replay_data["saved"].keys()):
        for replay in replay_data["saved"][replay_data["currentCharConfig"]]:
            if replay in player_data["user"]["dungeon"]["stages"]:
                player_data["user"]["dungeon"]["stages"][replay]["hasBattleReplay"] = 1

    squads_data = read_json(SQUADS_PATH)
    charId2instId = {}
    for character_index, character in player_data["user"]["troop"]["chars"].items():
        charId2instId[character["charId"]] = character["instId"]
    # 修改 #selectedCode 中的循环部分
    for i in squads_data:
        j = 0
        for slot in squads_data[i]["slots"]:
            if j == 12:
                break
            charId = slot["charId"]
            del slot["charId"]
            if charId in charId2instId:
                instId = charId2instId[charId]
                slot["charInstId"] = instId
                # 添加安全检查，确保角色存在且有装备字段
                instId_str = str(instId)  # 确保使用字符串键
                if (instId_str in player_data["user"]["troop"]["chars"] and
                        "equip" in player_data["user"]["troop"]["chars"][instId_str] and
                        slot["currentEquip"] not in player_data["user"]["troop"]["chars"][instId_str]["equip"]):
                    slot["currentEquip"] = None
            else:
                squads_data[i]["slots"][j] = None
            j += 1
        for k in range(j, 12):
            squads_data[i]["slots"].append(None)
        squads_data[i]["slots"] = squads_data[i]["slots"][:12]

    player_data["user"]["troop"]["squads"] = squads_data

    secretarySkinId = config["userConfig"]["secretarySkinId"]
    theme = config["userConfig"]["theme"]

    if (current_preset := player_data["user"]["charRotation"]["preset"].get(
            player_data["user"]["charRotation"]["current"]
    )):
        player_data["user"]["status"]["secretary"] = current_preset["profileInst"]
        player_data["user"]["background"]["selected"] = current_preset["background"]

    player_data["user"]["status"]["secretarySkinId"] = secretarySkinId
    player_data["user"]["homeTheme"]["selected"] = theme

    season = config["towerConfig"]["season"]

    player_data["user"]["tower"]["season"]["id"] = season

    story_review_groups = {}
    for i in story_review_table:
        story_review_groups[i] = {"rts": 1700000000, "stories": [], "trailRewards": []}
        for j in story_review_table[i]["infoUnlockDatas"]:
            story_review_groups[i]["stories"].append(
                {"id": j["storyId"], "uts": 1695000000, "rc": 1}
            )
        if i in story_review_meta_table["miniActTrialData"]["miniActTrialDataMap"]:
            for j in story_review_meta_table["miniActTrialData"]["miniActTrialDataMap"][
                i
            ]["rewardList"]:
                story_review_groups[i]["trailRewards"].append(j["trialRewardId"])
    player_data["user"]["storyreview"]["groups"] = story_review_groups

    enemies = {}
    if "enemyData" in enemy_handbook_table:
        for i in enemy_handbook_table["enemyData"]:
            enemies[i] = 1
    else:
        for i in enemy_handbook_table:
            enemies[i] = 1
    player_data["user"]["dexNav"]["enemy"]["enemies"] = enemies

    for i in activity_table["activity"]:
        if i not in player_data["user"]["activity"]:
            player_data["user"]["activity"][i] = {}
        for j in activity_table["activity"][i]:
            if j not in player_data["user"]["activity"][i]:
                player_data["user"]["activity"][i][j] = {}

    player_data["user"]["medal"] = {"medals": {}}
    for i in medal_table["medalList"]:
        medalId = i["medalId"]
        player_data["user"]["medal"]["medals"][medalId] = {
            "id": medalId,
            "val": [],
            "fts": 1695000000,
            "rts": 1695000000,
        }

    rlv2_table = get_memory("roguelike_topic_table")
    for theme in player_data["user"]["rlv2"]["outer"]:
        if theme in rlv2_table["details"]:
            player_data["user"]["rlv2"]["outer"][theme]["record"]["stageCnt"] = {
                i: 1 for i in rlv2_table["details"][theme]["stages"]
            }

    selected_crisis = config["crisisV2Config"]["selectedCrisis"]
    if selected_crisis:
        rune = read_json(f"{CRISIS_V2_JSON_BASE_PATH}{selected_crisis}.json")
        season = rune["info"]["seasonId"]
        player_data["user"]["crisisV2"]["current"] = season

    run_after_response(write_json, player_data, USER_JSON_PATH)

    b = datetime.now()
    print(f"syncdata耗时: {b - a}")
    return player_data


def accountSyncStatus():

    data = {
        "ts": round(time()),
        "result": {},
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    run_after_response(checkin.update_check_in_status)
    return data


def accountYostarAuthRequest():
    data = request.data
    data = {}

    return data


def accountYostarAuthSubmit():
    data = request.data
    data = {
        "result": 0,
        "yostar_account": "1234567890@123.com",
        "yostar_token": "a",
        "yostar_uid": "10000023"
    }

    return data


def syncPushMessage():
    # 数据同步参数，不做处理

    return {
        "code": 200,
        "msg": "OK",
    }
