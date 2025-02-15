import json
from os.path import exists
from virtualtime import time
from copy import deepcopy
from base64 import b64encode
from hashlib import md5
from flask import request
from datetime import datetime

from constants import (
    USER_JSON_PATH,
    CONFIG_PATH,
    BATTLE_REPLAY_JSON_PATH,
    SYNC_DATA_TEMPLATE_PATH,
    CRISIS_V2_JSON_BASE_PATH,
    MAILLIST_PATH,
    SQUADS_PATH,
    get_memory
)
from utils import read_json, write_json
import uuid

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

    return data


def accountSyncData():
    if not exists(USER_JSON_PATH):
        write_json({}, USER_JSON_PATH)

    saved_data = read_json(USER_JSON_PATH)
    mail_data = read_json(MAILLIST_PATH, encoding="utf-8")
    player_data = read_json(SYNC_DATA_TEMPLATE_PATH, encoding="utf-8")
    config = read_json(CONFIG_PATH)

    # Load newest data
    data_skin = get_memory("skin_table")
    character_table = get_memory("character_table")
    equip_table = get_memory("uniequip_table")
    battle_equip_table = get_memory("battle_equip_table")
    display_meta_table = get_memory("display_meta_table")
    retro_table = get_memory("retro_table")
    charm_table = get_memory("charm_table")
    activity_table = get_memory("activity_table")
    charword_table = get_memory("charword_table")

    ts = round(time())
    cnt = 0
    cntInstId = 1
    maxInstId = 1
    tempSkinTable = {}
    myCharList = {}
    charGroup = {}
    buildingChars = {}

    # charRotation
    default_char_rotation = {
        "current": "1",
        "preset": {
            "1": {
                "background": "bg_rhodes_day",
                "homeTheme": "tm_rhodes_day",
                "name": "unname",
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
    player_data["user"].setdefault("charRotation", default_char_rotation)
    saved_data["user"]["charRotation"] = player_data["user"]["charRotation"]
    target_current = player_data["user"]["charRotation"]["current"]
    use_profile = player_data["user"]["charRotation"]["preset"][target_current]["profile"]
    for slots in player_data["user"]["charRotation"]["preset"][target_current]["slots"]:
        if slots.get("skinId") == use_profile:
            use_charid = slots.get("charId")
            break
    player_data["user"]["status"]["secretary"] = use_charid
    player_data["user"]["status"]["secretarySkinId"] = use_profile
    player_data["user"]["background"]["selected"] = player_data["user"]["charRotation"]["preset"][target_current]["background"]


    # Tamper Skins
    skinKeys = list(data_skin["charSkins"].keys())
    player_data["user"]["skin"]["characterSkins"] = {}
    for i in data_skin["charSkins"].values():
        if "@" not in skinKeys[cnt]:
            # Not Special Skins
            cnt += 1
            continue

        player_data["user"]["skin"]["characterSkins"][skinKeys[cnt]] = 1
        if (
            i["charId"] not in tempSkinTable.keys()
            or i["displaySkin"]["onYear"]
            > data_skin["charSkins"][tempSkinTable[i["charId"]]]["displaySkin"]["onYear"]
            ):
            tempSkinTable[i["charId"]] = i["skinId"]
        cnt += 1

    # Tamper Operators
    edit_json = config["charConfig"]

    cnt = 0
    operatorKeys = list(character_table.keys())
    equip_keys = set(equip_table["charEquip"].keys())
    player_data_keys = set(player_data["user"]["troop"]["chars"].keys())

    for operatorKey in operatorKeys:
        if "char" not in operatorKey:
            continue

        charGroup.update({operatorKey: {"favorPoint": 25570}})

    for i in character_table:
        if i in player_data_keys:
            myCharList[int(cntInstId)] = player_data["user"]["troop"]["chars"][i]
        else:
            if "char" not in operatorKeys[cnt]:
                cnt += 1
                continue

            # Add all operators
            if edit_json["level"] == -1:
                level = character_table[i]["phases"][edit_json["evolvePhase"]]["maxLevel"]
            else:
                level = edit_json["level"]

            maxEvolvePhase = len(character_table[i]["phases"]) - 1
            evolvePhase = maxEvolvePhase

            if edit_json["evolvePhase"] != -1:
                if edit_json["evolvePhase"] > maxEvolvePhase:
                    evolvePhase = maxEvolvePhase
                else:
                    evolvePhase = edit_json["evolvePhase"]
            voiceLan = "JP"
            if operatorKeys[cnt] in charword_table["charDefaultTypeDict"]:
                voiceLan = charword_table["charDefaultTypeDict"][operatorKeys[cnt]]
            cntInstId = int(operatorKeys[cnt].split("_")[1])
            maxInstId = max(maxInstId, cntInstId)
            myCharList[int(cntInstId)] = {
                "instId": int(cntInstId),
                "charId": operatorKeys[cnt],
                "favorPoint": edit_json["favorPoint"],
                "potentialRank": edit_json["potentialRank"],
                "mainSkillLvl": edit_json["mainSkillLvl"],
                "skin": str(operatorKeys[cnt]) + "#1",
                "level": level,
                "exp": 0,
                "evolvePhase": evolvePhase,
                "defaultSkillIndex": len(character_table[i]["skills"]) - 1,
                "gainTime": int(time()),
                "skills": [],
                "voiceLan": voiceLan,
                "currentEquip": None,
                "equip": {},
                "starMark": 0,
            }

            # set to E2 art if available skipping is2 recruits
            if operatorKeys[cnt] not in [
                "char_508_aguard",
                "char_509_acast",
                "char_510_amedic",
                "char_511_asnipe",
            ]:
                if myCharList[int(cntInstId)]["evolvePhase"] == 2:
                    if int(cntInstId) in [609, 610, 611, 612, 613, 614, 615]:
                        myCharList[int(cntInstId)]["skin"] = str(operatorKeys[cnt]) + "#1"
                    else:
                        myCharList[int(cntInstId)]["skin"] = str(operatorKeys[cnt]) + "#2"

            # set to seasonal skins
            if operatorKeys[cnt] in tempSkinTable.keys():
                myCharList[int(cntInstId)]["skin"] = tempSkinTable[operatorKeys[cnt]]

            # Add Skills
            for index, skill in enumerate(character_table[i]["skills"]):
                myCharList[int(cntInstId)]["skills"].append(
                    {
                        "skillId": skill["skillId"],
                        "unlock": 1,
                        "state": 0,
                        "specializeLevel": 0,
                        "completeUpgradeTime": -1,
                    }
                )

                # M3
                if len(skill["levelUpCostCond"]) > 0:
                    myCharList[int(cntInstId)]["skills"][index]["specializeLevel"] = (
                        edit_json["skillsSpecializeLevel"]
                    )

            # Add equips
            if myCharList[int(cntInstId)]["charId"] in equip_keys:
                for equip in equip_table["charEquip"][myCharList[int(cntInstId)]["charId"]]:
                    level = 1
                    if equip in list(battle_equip_table.keys()):
                        level = len(battle_equip_table[equip]["phases"])
                    myCharList[int(cntInstId)]["equip"].update(
                        {equip: {"hide": 0, "locked": 0, "level": level}}
                    )
                myCharList[int(cntInstId)]["currentEquip"] = equip_table["charEquip"][
                    myCharList[int(cntInstId)]["charId"]
                ][-1]

            # Dexnav
            player_data["user"]["dexNav"]["character"][operatorKeys[cnt]] = {
                "charInstId": cntInstId,
                "count": 6,
            }

            custom_units = edit_json["customUnitInfo"]

            for char in custom_units:
                if operatorKeys[cnt] == char:
                    for key in custom_units[char]:
                        if key != "skills":
                            myCharList[int(cntInstId)][key] = custom_units[char][key]
                        else:
                            for skillIndex, skillValue in enumerate(
                                custom_units[char]["skills"]
                            ):
                                myCharList[int(cntInstId)]["skills"][skillIndex][
                                    "specializeLevel"
                                ] = skillValue

            # Amiya info
            if operatorKeys[cnt] == "char_002_amiya":
                myCharList[int(cntInstId)].update(
                    {
                        "defaultSkillIndex": -1,
                        "skills": [],
                        "currentTmpl": "char_002_amiya",
                        "tmpl": {
                            "char_002_amiya": {
                                "skinId": "char_002_amiya@test#1",
                                "defaultSkillIndex": 2,
                                "skills": [
                                    {
                                        "skillId": skill_name,
                                        "unlock": 1,
                                        "state": 0,
                                        "specializeLevel": edit_json[
                                            "skillsSpecializeLevel"
                                        ],
                                        "completeUpgradeTime": -1,
                                    }
                                    for skill_name in [
                                        "skcom_magic_rage[3]",
                                        "skchr_amiya_2",
                                        "skchr_amiya_3",
                                    ]
                                ],
                                "currentEquip": None,
                                "equip": {},
                            },
                            "char_1001_amiya2": {
                                "skinId": "char_1001_amiya2@casc#1",
                                "defaultSkillIndex": 1,
                                "skills": [
                                    {
                                        "skillId": skill_name,
                                        "unlock": 1,
                                        "state": 0,
                                        "specializeLevel": edit_json[
                                            "skillsSpecializeLevel"
                                        ],
                                        "completeUpgradeTime": -1,
                                    }
                                    for skill_name in ["skchr_amiya2_1", "skchr_amiya2_2"]
                                ],
                                "currentEquip": None,
                                "equip": {},
                            },
                            "char_1037_amiya3": {
                                "skinId": "char_1001_amiya2@casc#1",
                                "defaultSkillIndex": 1,
                                "skills": [
                                    {
                                        "skillId": skill_name,
                                        "unlock": 1,
                                        "state": 0,
                                        "specializeLevel": edit_json[
                                            "skillsSpecializeLevel"
                                        ],
                                        "completeUpgradeTime": -1,
                                    }
                                    for skill_name in ["skchr_amiya3_1", "skchr_amiya3_2"]
                                ],
                                "currentEquip": None,
                                "equip": {},
                            },
                        },
                    }
                )
                for equip in equip_table["charEquip"]["char_002_amiya"]:
                    level = 1
                    if equip in list(battle_equip_table.keys()):
                        level = len(battle_equip_table[equip]["phases"])
                    myCharList[int(cntInstId)]["tmpl"]["char_002_amiya"]["equip"].update(
                        {equip: {"hide": 0, "locked": 0, "level": level}}
                    )
                myCharList[int(cntInstId)]["tmpl"]["char_002_amiya"]["currentEquip"] = (
                    equip_table["charEquip"]["char_002_amiya"][-1]
                )
            elif operatorKeys[cnt] == "char_512_aprot":
                myCharList[int(cntInstId)]["skin"] = "char_512_aprot#1"

            buildingChars.update(
                {
                    int(cntInstId): {
                        "charId": operatorKeys[cnt],
                        "lastApAddTime": round(time()) - 3600,
                        "ap": 8640000,
                        "roomSlotId": "",
                        "index": -1,
                        "changeScale": 0,
                        "bubble": {
                            "normal": {"add": -1, "ts": 0},
                            "assist": {"add": -1, "ts": 0},
                        },
                        "workTime": 0,
                    }
                }
            )

            cnt += 1
    cntInstId = maxInstId+1

    dupe_characters = edit_json["duplicateUnits"]
    for dupeChar in dupe_characters:
        tempChar = {}
        for char in myCharList:
            if dupeChar == myCharList[char]["charId"]:
                tempChar = deepcopy(myCharList[char])
                break

        tempChar["instId"] = int(cntInstId)
        myCharList[int(cntInstId)] = tempChar
        cntInstId += 1

    player_data["user"]["troop"]["chars"] = myCharList
    player_data["user"]["troop"]["charGroup"] = charGroup
    player_data["user"]["troop"]["curCharInstId"] = cntInstId

    # Tamper story
    myStoryList = {"init": 1}
    story_table = get_memory("story_table")
    for story in story_table:
        myStoryList.update({story:1})

    player_data["user"]["status"]["flags"] = myStoryList

    # Tamper Stages
    myStageList = {}
    stage_table = get_memory("stage_table")
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
    addon_table = get_memory("handbook_info_table")
    for charId in addon_table["handbookDict"]:
        addonList[charId] = {"story":{}}
        story = addon_table["handbookDict"][charId]["handbookAvgList"]
        for i,j in zip(story,range(len(story))):
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

    player_data["user"]["troop"]["addon"].update(addonList) # TODO: I might try MongoDB in the future.

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
        trail.update({retro:{}})
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
            player_data["user"]["campaignsV2"]["open"]["permanent"].append(stage)
            player_data["user"]["campaignsV2"]["open"]["training"].append(stage)

    # Tamper Avatars and Backgrounds
    avatar_icon = {}
    for avatar in display_meta_table["playerAvatarData"]["avatarList"]:
        avatar_icon.update({
            avatar["avatarId"]: {
                "ts": round(time()),
                "src": "initial" if avatar["avatarId"].startswith("avatar_def") else "other"
            }
        })
    player_data["user"]["avatar"]["avatar_icon"] = avatar_icon

    bgs = {}
    for bg in display_meta_table["homeBackgroundData"]["homeBgDataList"]:
        bgs.update({
            bg["bgId"]: {
                "unlock": round(time())
            }
        })
    player_data["user"]["background"]["bgs"] = bgs

    if "themeList" in display_meta_table["homeBackgroundData"]:
        themes = {}
        for theme in display_meta_table["homeBackgroundData"]["themeList"]:
            themes[theme["id"]] = {"unlock": 1691670000}
        player_data["user"]["homeTheme"]["themes"] = themes

    # Update charms
    for charm in charm_table["charmList"]:
        player_data["user"]["charm"]["charms"].update({charm["id"]: 1})

    # Update battle bus
    if "carData" in activity_table:
        for car_gear in activity_table["carData"]["carDict"]:
            player_data["user"]["car"]["accessories"].update({
                car_gear: {
                    "id": car_gear,
                    "num": len(activity_table["carData"]["carDict"][car_gear]["posList"])
                }
            })

    # Update Stultifera Navis
    activity_data = activity_table["activity"]["TYPE_ACT17SIDE"]["act17side"]
    for place in activity_data["placeDataMap"]:
        player_data["user"]["deepSea"]["places"].update({place: 2})

    for node in activity_data["nodeInfoDataMap"]:
        player_data["user"]["deepSea"]["nodes"].update({node: 2})

    for choice_node in activity_data["choiceNodeDataMap"]:
        player_data["user"]["deepSea"]["choices"].update({
            choice_node: [2 for _ in activity_data["choiceNodeDataMap"][choice_node]["optionList"]]
        })

    for event in activity_data["eventDataMap"]:
        player_data["user"]["deepSea"]["events"].update({event: 1})

    for treasure in activity_data["treasureNodeDataMap"]:
        player_data["user"]["deepSea"]["treasures"].update({treasure: 1})

    for story in activity_data["storyNodeDataMap"]:
        player_data["user"]["deepSea"]["stories"].update({
            activity_data["storyNodeDataMap"][story]["storyKey"]: 1
        })

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
            player_data["user"]["deepSea"]["logs"].update({chapter:[log]})

    # Check if mail exists
    for mailId in mail_data["mailList"]:
        if (
            int(mailId) not in mail_data["recievedIDs"]
            and int(mailId) not in mail_data["deletedIDs"]
        ):
            player_data["user"]["pushFlags"]["hasGifts"] = 1
            break

    # Update timestamps
    player_data["user"]["status"]["lastRefreshTs"] = ts
    player_data["user"]["status"]["lastApAddTime"] = ts
    player_data["user"]["status"]["registerTs"] = ts
    player_data["user"]["status"]["lastOnlineTs"] = ts
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
                if (
                    slot["currentEquip"]
                    not in player_data["user"]["troop"]["chars"][instId]["equip"]
                ):
                    slot["currentEquip"] = None
            else:
                squads_data[i]["slots"][j] = None
            j += 1
        for k in range(j, 12):
            squads_data[i]["slots"].append(None)
        squads_data[i]["slots"] = squads_data[i]["slots"][:12]

    player_data["user"]["troop"]["squads"] = squads_data

    # Copy over from previous launch if data exists
    if (
        "user" in saved_data
        and config["userConfig"]["restorePreviousStates"]["squadsAndFavs"]
    ):
        player_data["user"]["troop"]["squads"] = saved_data["user"]["troop"]["squads"]

        for _, saved_character in saved_data["user"]["troop"]["chars"].items():
            index = None
            for character_index, character in player_data["user"]["troop"][
                "chars"
            ].items():
                if saved_character["charId"] == character["charId"]:
                    index = character_index
                    break

            if index is not None:
                player_data["user"]["troop"]["chars"][index]["starMark"] = (saved_character["starMark"])
                player_data["user"]["troop"]["chars"][index]["voiceLan"] = (saved_character["voiceLan"])
                player_data["user"]["troop"]["chars"][index]["skin"] = saved_character["skin"]
                player_data["user"]["troop"]["chars"][index]["defaultSkillIndex"] = (saved_character["defaultSkillIndex"])
                if saved_character["currentEquip"]:
                    player_data["user"]["troop"]["chars"][index]["currentEquip"] = (saved_character["currentEquip"])

    secretary = config["userConfig"]["secretary"]
    secretarySkinId = config["userConfig"]["secretarySkinId"]
    background = config["userConfig"]["background"]
    theme = config["userConfig"]["theme"]

    if "user" in saved_data and config["userConfig"]["restorePreviousStates"]["ui"]:
        secretary = saved_data["user"]["status"]["secretary"]
        secretarySkinId = saved_data["user"]["status"]["secretarySkinId"]
        background = saved_data["user"]["background"]["selected"]
        theme = saved_data["user"]["homeTheme"]["selected"]

    player_data["user"]["status"]["secretary"] = secretary
    player_data["user"]["status"]["secretarySkinId"] = secretarySkinId
    player_data["user"]["background"]["selected"] = background
    player_data["user"]["homeTheme"]["selected"] = theme

    season = config["towerConfig"]["season"]

    player_data["user"]["tower"]["season"]["id"] = season

    story_review_table = get_memory("story_review_table")
    story_review_meta_table = get_memory("story_review_meta_table")
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

    enemy_handbook_table = get_memory("enemy_handbook_table")
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
    medal_table = get_memory("medal_table")
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
        rune = read_json(
            f"{CRISIS_V2_JSON_BASE_PATH}{selected_crisis}.json", encoding="utf-8"
        )
        season = rune["info"]["seasonId"]
        player_data["user"]["crisisV2"]["current"] = season

    return player_data


def accountSyncStatus():
    
    data = request.data
    data = {
        "ts": round(time()),
        "result": {},
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

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
