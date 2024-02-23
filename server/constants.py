from utils import read_json

# Config Data
CONFIG_PATH = "config/config.json"
MAILLIST_PATH = "config/mails.json"
RLV2_CONFIG_PATH = "config/rlv2Config.json"
SQUADS_PATH = "config/squads.json"
SYNC_DATA_TEMPLATE_PATH = "syncData.json"

# User Data
USER_JSON_PATH = "data/user/user.json"
BATTLE_REPLAY_JSON_PATH = "data/user/battleReplays.json"
RLV2_JSON_PATH = "data/user/rlv2.json"
RLV2_TEMPBUFF_JSON_PATH = "data/user/rlv2TempBuffs.json"
CRISIS_JSON_BASE_PATH = "data/crisis/"
RUNE_JSON_PATH = "data/user/rune.json"

# RLV2 Options
RLV2_CHOICEBUFFS = "data/rlv2/choiceBuffs.json"
RLV2_RECRUITGROUPS = "data/rlv2/recruitGroups.json"
RLV2_NODESINFO = "data/rlv2/nodesInfo.json"

# TOWER Data
TOWERDATA_PATH = "data/tower/towerData.json"

config = read_json(CONFIG_PATH)
mode = config["server"]["mode"]
if mode == "global":
    BASE_URL = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata"
elif mode == "cn":
    BASE_URL = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata"

# TABLE Urls
ACTIVITY_TABLE_URL = BASE_URL + "/excel/activity_table.json"
CHARM_TABLE_URL = BASE_URL + "/excel/charm_table.json"
SKIN_TABLE_URL = BASE_URL + "/excel/skin_table.json"
CHARACTER_TABLE_URL = BASE_URL + "/excel/character_table.json"
BATTLEEQUIP_TABLE_URL = BASE_URL + "/excel/battle_equip_table.json"
EQUIP_TABLE_URL = BASE_URL + "/excel/uniequip_table.json"
STORY_TABLE_URL = BASE_URL + "/excel/story_table.json"
STAGE_TABLE_URL = BASE_URL + "/excel/stage_table.json"
RL_TABLE_URL = BASE_URL + "/excel/roguelike_topic_table.json"
DM_TABLE_URL = BASE_URL + "/excel/display_meta_table.json"
RETRO_TABLE_URL = BASE_URL + "/excel/retro_table.json"
HANDBOOK_INFO_TABLE_URL = BASE_URL + "/excel/handbook_info_table.json"
TOWER_TABLE_URL = BASE_URL + "/excel/climb_tower_table.json"