import json
import os

def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_info_by_char_id(user_data, char_id):
    troop = user_data.get("user", {}).get("troop", {})
    for _, char_info in troop.get("chars", {}).items():
        if char_info.get("charId") == char_id:
            return char_info.get("currentEquip"), char_info.get("defaultSkillIndex")
    return None, None

def main():
    base_path = os.path.dirname(__file__)
    char_table_path = os.path.join(base_path, "../data/excel/character_table.json")
    config_path = os.path.join(base_path, "config.json")
    user_file_path = os.path.join(base_path, "../data/user/user.json")
    output_path = os.path.join(base_path, "../config/assist.json")

    # 读取数据
    characters = read_json(char_table_path)
    config = read_json(config_path)
    user_data = read_json(user_file_path)

    rarity_filter = config.get("rarity", {})
    profession_limit = config.get("profession_limit", {})

    assist_data = {}
    added_char_ids = set()

    def rarity_sort_key(item):
        rarity = item["rarity"]
        return int(rarity.split("_")[1]) if "TIER_" in rarity else 0

    # 分类
    for char_id, info in characters.items():
        rarity = info.get("rarity")
        profession = info.get("profession")

        # 过滤条件：跳过 TOKEN profession 和禁用稀有度
        if profession == "TOKEN" or rarity_filter.get(rarity) is False:
            continue

        current_equip, default_skill_index = get_info_by_char_id(user_data, char_id)
        char_entry = {
            "charId": char_id,
            "skillIndex": default_skill_index,
            "currentEquip": current_equip,
            "rarity": rarity
        }

        if profession not in assist_data:
            assist_data[profession] = []
        assist_data[profession].append(char_entry)

    # 按稀有度排序并限制数量
    for prof, chars in assist_data.items():
        chars.sort(key=rarity_sort_key, reverse=True)
        limit = profession_limit.get(prof, len(chars))
        if limit > len(chars):
            limit = len(chars)   # 修复：限制数大于角色数时只生成现有数量
        assist_data[prof] = chars[:limit]

        # 删除临时 rarity 字段
        for c in assist_data[prof]:
            c.pop("rarity", None)

    write_json(assist_data, output_path)
    print(f"生成完成: {output_path}")
if __name__ == "__main__":
    main()
