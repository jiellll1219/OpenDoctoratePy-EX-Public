from msgspec.json import Decoder
from utils import read_json

# Config Data
CONFIG_PATH = "config/config.json"
EX_CONFIG_PATH  = "config/exConfig.json"
MAILLIST_PATH = "config/mails.json"
MAILCOLLECTION_PATH = "config/mailCollection.json"
RLV2_CONFIG_PATH = "config/rlv2Config.json"
SQUADS_PATH = "config/squads.json"
SYNC_DATA_TEMPLATE_PATH = "data/user/user.json"

# Gacha Data
NORMALGACHA_PATH = "data/gacha/normalGacha.json"
GACHA_HISTORY_PATH = "data/user/gachaHistory.json"
EX_GACHA_DATA_PATH = "data/user/exGachaData.json"

# User Data
USER_JSON_PATH = "data/user/user.json"
BATTLE_REPLAY_JSON_PATH = "data/user/battleReplays.json"
RLV2_JSON_PATH = "data/user/rlv2.json"
RLV2_TEMPBUFF_JSON_PATH = "data/user/rlv2TempBuffs.json"
RLV2_USER_SETTINGS_PATH = "data/user/rlv2UserSettings.json"
RLV2_SETTINGS_PATH = "data/user/rlv2Settings.json"
CRISIS_JSON_BASE_PATH = "data/crisis/"
CRISIS_V2_JSON_BASE_PATH = "data/crisisV2/"
RUNE_JSON_PATH = "data/user/rune.json"

# RLV2 Options
RLV2_CHOICEBUFFS = "data/rlv2/choiceBuffs.json"
RLV2_RECRUITGROUPS = "data/rlv2/recruitGroups.json"
RLV2_NODESINFO = "data/rlv2/nodesInfo.json"

# TOWER Data
TOWERDATA_PATH = "data/tower/towerData.json"

# TABLE Urls
ACTIVITY_TABLE_PATH = "data/excel/activity_table.json"
CHARM_TABLE_PATH = "data/excel/charm_table.json"
SKIN_TABLE_PATH = "data/excel/skin_table.json"
CHARACTER_TABLE_PATH = "data/excel/character_table.json"
BATTLEEQUIP_TABLE_PATH = "data/excel/battle_equip_table.json"
EQUIP_TABLE_PATH = "data/excel/uniequip_table.json"
STORY_TABLE_PATH = "data/excel/story_table.json"
STAGE_TABLE_PATH = "data/excel/stage_table.json"
RL_TABLE_PATH = "data/excel/roguelike_topic_table.json"
DM_TABLE_PATH = "data/excel/display_meta_table.json"
RETRO_TABLE_PATH = "data/excel/retro_table.json"
HANDBOOK_INFO_TABLE_PATH = "data/excel/handbook_info_table.json"
TOWER_TABLE_PATH = "data/excel/climb_tower_table.json"
BUILDING_TABLE_PATH = "data/excel/building_data.json"
STORY_REVIEW_TABLE_PATH = "data/excel/story_review_table.json"
ENEMY_HANDBOOK_TABLE_PATH = "data/excel/enemy_handbook_table.json"
MEDAL_TABLE_PATH = "data/excel/medal_table.json"
SANDBOX_TABLE_PATH = "data/excel/sandbox_perm_table.json"
CHARWORD_TABLE_PATH = "data/excel/charword_table.json"
STORY_REVIEW_META_TABLE_PATH = "data/excel/story_review_meta_table.json"
GACHA_TABLE_PATH = "data/excel/gacha_table.json"

# Table In Memory

#定义一个全局变量，用于存储从 JSON 文件中读取的数据
memory_cache = {}
useMemoryCache = read_json(EX_CONFIG_PATH)["useMemoryCache"]
# 读取 JSON 文件并存入内存
def preload_json_data():
    global memory_cache
    paths = {
        "activity_table": ACTIVITY_TABLE_PATH,
        "charm_table": CHARM_TABLE_PATH,
        "skin_table": SKIN_TABLE_PATH,
        "character_table": CHARACTER_TABLE_PATH,
        "battle_equip_table": BATTLEEQUIP_TABLE_PATH,
        "uniequip_table": EQUIP_TABLE_PATH,
        "story_table": STORY_TABLE_PATH,
        "stage_table": STAGE_TABLE_PATH,
        "roguelike_topic_table": RL_TABLE_PATH,
        "display_meta_table": DM_TABLE_PATH,
        "retro_table": RETRO_TABLE_PATH,
        "handbook_info_table": HANDBOOK_INFO_TABLE_PATH,
        "tower_table": TOWER_TABLE_PATH,
        "building_data": BUILDING_TABLE_PATH,
        "story_review_table": STORY_REVIEW_TABLE_PATH,
        "enemy_handbook_table": ENEMY_HANDBOOK_TABLE_PATH,
        "medal_table": MEDAL_TABLE_PATH,
        "sandbox_table": SANDBOX_TABLE_PATH,
        "charword_table": CHARWORD_TABLE_PATH,
        "story_review_meta_table": STORY_REVIEW_META_TABLE_PATH,
        "gacha_table": GACHA_TABLE_PATH
    }
    
    for key, path in paths.items():
        with open(path, 'r', encoding='utf-8') as f:
            # 使用 msgspec 解码器解码
            memory_cache[key] = Decoder(strict=False).decode(f.read())

# 直接从内存中获取数据
def get_memory(key: str):
    if useMemoryCache:
        try:
            return memory_cache.get(key)
        except Exception:
            print("Error: Failed to load {key} from memory")
            return read_json(f"data/excel/{key}.json")
    else:
        return read_json(f"data/excel/{key}.json", encoding='utf-8')

# Shop Data
ALLPRODUCTLIST_PATH = "data/shop/AllProductList.json"
CASHGOODLIST_PATH = "data/shop/CashGoodList.json"
EPGSGOODLIST_PATH = "data/shop/EPGSGoodList.json"
EXTRAGOODLIST_PATH = "data/shop/ExtraGoodList.json"
FURNIGOODLIST_PATH = "data/shop/FurniGoodList.json"
GPGOODLIST_PATH = "data/shop/GPGoodList.json"
HIGHGOODLIST_PATH = "data/shop/HighGoodList.json"
LMTGSGOODLIST_PATH = "data/shop/LMTGSGoodList.json"
LOWGOODLIST_PATH = "data/shop/LowGoodList.json"
REPGOODLIST_PATH = "data/shop/RepGoodList.json"
SKINGOODLIST_PATH = "data/shop/SkinGoodList.json"
SOCIALGOODLIST_PATH = "data/shop/SocialGoodList.json"
CLASSICGOODLIST_PATH = "data/shop/ClassicGoodList.json"

# Activity Shop Data
TEMPLATEGOODLIST_PATH = "data/shop/templateGoodList.json"