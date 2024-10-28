from utils import read_json

# Config Data
CONFIG_PATH = "config/config.json"
EX_CONFIG_PATH  = "config/exConfig.json"
MAILLIST_PATH = "config/mails.json"
RLV2_CONFIG_PATH = "config/rlv2Config.json"
SQUADS_PATH = "config/squads.json"
SYNC_DATA_TEMPLATE_PATH = "syncData.json"
CHARWORD_TABLE_URL = "data/excel/charword_table.json"

# Gacha Data
NORMALGACHA_PATH = "data/gacha/normalGacha.json"

# User Data
USER_JSON_PATH = "data/user/user.json"
BATTLE_REPLAY_JSON_PATH = "data/user/battleReplays.json"
RLV2_JSON_PATH = "data/user/rlv2.json"
RLV2_TEMPBUFF_JSON_PATH = "data/user/rlv2TempBuffs.json"
RLV2_USER_SETTINGS_PATH = "data/user/rlv2UserSettings.json"
RLV2_SETTINGS_PATH = "data/user/rlv2Settings.json"
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

# Shop Data
ALLPRODUCTLIST_PATH = "data/shop/AllProductList.json"
CASHGOODLIST_PATH = "data/shop/CashGoodList.json"
EPGSGOODLIST_PATH = "data/shop/EPGSGoodList.json"
EXTRAGOODLIST_PATH = "data/shop/ExtraGoodList.json"
FURNIGOODLIST_PATH = "data/shop/FurniGoodList.json"
GPGOODLIST_PATH = "data/shop/GPGoodList.json"
HIGHGOODLIST_PATH = "data/shop/HighGoodList.json"
LMTGOODLIST_PATH = "data/shop/LMTGoodList.json"
LOWGOODLIST_PATH = "data/shop/LowGoodList.json"
REPGOODLIST_PATH = "data/shop/RepGoodList.json"
SKINGOODLIST_PATH = "data/shop/SkinGoodList.json"
SOCIALGOODLIST_PATH = "data/shop/SocialGoodList.json"
CLASSICGOODLIST_PATH = "data/shop/ClassicGoodList.json"

# Activity Shop Data
TEMPLATEGOODLIST_PATH = "data/shop/templateGoodList.json"