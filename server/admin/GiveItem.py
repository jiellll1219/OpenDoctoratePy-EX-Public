from datetime import datetime
from constants import USER_JSON_PATH
from utils import read_json, write_json

def GiveItem(reward_id, reward_type, reward_count, items):
    user_data = read_json(USER_JSON_PATH)
    
    chars = user_data["troop"]["chars"]
    troop = {}

    if reward_type == "CHAR":
        item = {}
        randomCharId = reward_id
        repeatCharId = 0

        for j in range(len(user_data["troop"]["chars"])):
            if user_data["troop"]["chars"][str(j + 1)]["charId"] == randomCharId:
                repeatCharId = j + 1
                break

        if repeatCharId == 0:
            get_char = {}
            char_data = {}
            skilsArray = user_data[randomCharId]["skills"]
            skils = []

            for m in range(len(skilsArray)):
                new_skils = {}
                new_skils["skillId"] = skilsArray[m]["skillId"]
                new_skils["state"] = 0
                new_skils["specializeLevel"] = 0
                new_skils["completeUpgradeTime"] = -1
                if skilsArray[m]["unlockCond"]["phase"] == 0:
                    new_skils["unlock"] = 1
                else:
                    new_skils["unlock"] = 0
                skils.append(new_skils)

            instId = len(user_data["troop"]["chars"]) + 1
            char_data["instId"] = instId
            char_data["charId"] = randomCharId
            char_data["favorPoint"] = 0
            char_data["potentialRank"] = 0
            char_data["mainSkillLvl"] = 1
            char_data["skin"] = randomCharId + "#1"
            char_data["level"] = 1
            char_data["exp"] = 0
            char_data["evolvePhase"] = 0
            char_data["gainTime"] = int(datetime.now().timestamp())
            char_data["skills"] = skils
            char_data["voiceLan"] = user_data["charwordTable"]["charDefaultTypeDict"][randomCharId]
            char_data["defaultSkillIndex"] = -1 if skils == [] else 0

            sub1 = randomCharId[randomCharId.index("_") + 1:]
            charName = sub1[sub1.index("_") + 1:]

            if "uniequip_001_" + charName in user_data["uniequipTable"]:
                equip = {}
                uniequip_001 = {"hide": 0, "locked": 0, "level": 1}
                uniequip_002 = {"hide": 0, "locked": 0, "level": 1}
                equip["uniequip_001_" + charName] = uniequip_001
                equip["uniequip_002_" + charName] = uniequip_002
                char_data["equip"] = equip
                char_data["currentEquip"] = "uniequip_001_" + charName
            else:
                char_data["currentEquip"] = None

            user_data["troop"]["chars"][str(instId)] = char_data
            user_data["troop"]["curCharInstId"] = instId + 1
            user_data["troop"]["charGroup"][randomCharId] = {"favorPoint": 0}

            buildingChar = {"charId": randomCharId, "lastApAddTime": int(datetime.now().timestamp()),
                            "ap": 8640000, "roomSlotId": "", "index": -1, "changeScale": 0,
                            "bubble": {"normal": {"add": -1, "ts": 0}, "assist": {"add": -1, "ts": -1}},
                            "workTime": 0}
            user_data["building"]["chars"][str(instId)] = buildingChar

            get_char["charInstId"] = instId
            get_char["charId"] = randomCharId
            get_char["isNew"] = 1

            itemGet = []
            new_itemGet_1 = {"type": "HGG_SHD", "id": "4004", "count": 1}
            itemGet.append(new_itemGet_1)

            user_data["status"]["hggShard"] += 1

            get_char["itemGet"] = itemGet
            user_data["inventory"]["p_" + randomCharId] = 0

            charGet = get_char

            charinstId = {str(instId): char_data}
            chars[str(instId)] = char_data
            troop["chars"] = charinstId

            item["id"] = randomCharId
            item["type"] = reward_type
            item["charGet"] = charGet
            items.append(item)
        else:
            get_char = {}
            get_char["charInstId"] = repeatCharId
            get_char["charId"] = randomCharId
            get_char["isNew"] = 0

            repatChar = user_data["troop"]["chars"][str(repeatCharId)]

            potentialRank = repatChar["potentialRank"]
            rarity = user_data[randomCharId]["rarity"]

            itemName = None
            itemType = None
            itemId = None
            itemCount = 0
            if rarity in [0, 1, 2, 3]:
                itemName = "lggShard"
                itemType = "LGG_SHD"
                itemId = "4005"
                itemCount = 1 if rarity in [0, 1] else (5 if rarity == 2 else 30)
            elif rarity in [4, 5]:
                itemName = "hggShard"
                itemType = "HGG_SHD"
                itemId = "4004"
                itemCount = 5 if potentialRank != 5 else 8 if rarity == 4 else 10 if potentialRank != 5 else 15

            itemGet = []
            new_itemGet_1 = {"type": itemType, "id": itemId, "count": itemCount}
            itemGet.append(new_itemGet_1)
            user_data["status"][itemName] += itemCount

            new_itemGet_3 = {"type": "MATERIAL", "id": "p_" + randomCharId, "count": 1}
            itemGet.append(new_itemGet_3)
            user_data["inventory"]["p_" + randomCharId] += 1

            charGet = get_char

            charinstId = {str(repeatCharId): user_data["troop"]["chars"][str(repeatCharId)]}
            chars[str(repeatCharId)] = user_data["troop"]["chars"][str(repeatCharId)]
            troop["chars"] = charinstId

            item["type"] = reward_type
    if reward_type == "HGG_SHD":
        user_data['status']['practiceTicket'] += reward_count

    if reward_type == "LGG_SHD":
        user_data['status']['practiceTicket'] += reward_count

    if reward_type == "MATERIAL":
        user_data['inventory'][reward_id] += reward_count

    if reward_type == "CARD_EXP":
        user_data['inventory'][reward_id] += reward_count

    if reward_type == "SOCIAL_PT":
        user_data['status']['socialPoint'] += reward_count

    if reward_type == "AP_GAMEPLAY":
        user_data['status']['ap'] += reward_count

    if reward_type == "AP_ITEM":
        if "60" in reward_id:
            user_data['status']['ap'] += 60
        elif "200" in reward_id:
            user_data['status']['ap'] += 200
        else:
            user_data['status']['ap'] += 100

    if reward_type == "TKT_TRY":
        user_data['status']['practiceTicket'] += reward_count

    if reward_type == "DIAMOND":
        user_data['status']['androidDiamond'] += reward_count
        user_data['status']['iosDiamond'] += reward_count

    if reward_type == "DIAMOND_SHD":
        user_data['status']['diamondShard'] += reward_count

    if reward_type == "GOLD":
        user_data['status']['gold'] += reward_count

    if reward_type == "TKT_RECRUIT":
        user_data['status']['recruitLicense'] += reward_count

    if reward_type == "TKT_INST_FIN":
        user_data['status']['instantFinishTicket'] += reward_count

    if reward_type == "TKT_GACHA_PRSV":
        user_data['inventory'][reward_id] += reward_count

    if reward_type == "RENAMING_CARD":
        user_data['inventory'][reward_id] += reward_count

    if reward_type == "RETRO_COIN":
        user_data['inventory'][reward_id] += reward_count

    if reward_type == "AP_SUPPLY":
        user_data['inventory'][reward_id] += reward_count

    if reward_type == "TKT_GACHA_10":
        user_data['status']['tenGachaTicket'] += reward_count

    if reward_type == "TKT_GACHA":
        user_data['status']['gachaTicket'] += reward_count

    if "VOUCHER" in reward_type:
        if reward_id not in user_data['consumable']:
            consumables = {"0": {"ts": -1, "count": 0}}
            user_data['consumable'][reward_id] = consumables
        user_data['consumable'][reward_id]["0"]["count"] += reward_count

    if reward_type == "CHAR_SKIN":
        user_data['skin']['characterSkins'][reward_id] = 1
        user_data['skin']['skinTs'][reward_id] = int(datetime.now().timestamp())

    if reward_type != "CHAR":
        item = {"id": reward_id, "type": reward_type, "count": reward_count}
        items.append(item)

    else:
        return {
            "statusCode": 400,
            "error": "Bad Request",
            "message": "Not Found Info"
        }

    write_json(user_data, USER_JSON_PATH)