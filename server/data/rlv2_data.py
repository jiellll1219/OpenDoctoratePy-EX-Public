rogue_buffs = {
    "rogue_1": [],
    "rogue_2": [
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
    ],
    "rogue_3": [
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
    ],
    "rogue_4": [],
    "rogue_5": []
}

zone_1_nodes_demo = {
    "nodes":{
        "0": {
            "index": "0",
            "pos": {
                "x": 0,
                "y": 0
            },
            "next": [
                {
                    "x": 1,
                    "y": 0
                },
                {
                    "x": 1,
                    "y": 1
                }
            ],
            "type": 1,
            "refresh": "@refresh",
            "stage": "@stage"
        },
        "1": {
            "index": "1",
            "pos": {
                "x": 0,
                "y": 1
            },
            "next": [
                {
                    "x": 1,
                    "y": 2
                }
            ],
            "type": 1,
            "refresh": "@refresh",
            "stage": "@stage"
        },
        "100": {
            "index": "100",
            "pos": {
                "x": 1,
                "y": 0
            },
            "next": [
                {
                    "x": 2,
                    "y": 0
                },
                {
                    "x": 1,
                    "y": 1,
                    "key": True
                }
            ],
            "type": 32,
            "refresh": "@refresh"
        },
        "101": {
            "index": "101",
            "pos": {
                "x": 1,
                "y": 1
            },
            "next": [
                {
                    "x": 2,
                    "y": 0
                },
                {
                    "x": 1,
                    "y": 0,
                    "key": True
                },
                {
                    "x": 1,
                    "y": 2,
                    "key": True
                }
            ],
            "type": 512,
            "refresh": "@refresh"
        },
        "102": {
            "index": "102",
            "pos": {
                "x": 1,
                "y": 2
            },
            "next": [
                {
                    "x": 2,
                    "y": 1
                },
                {
                    "x": 1,
                    "y": 1,
                    "key": True
                }
            ],
            "type": 1,
            "refresh": "@refresh"
        },
        "200": {
            "index": "200",
            "pos": {
                "x": 2,
                "y": 0
            },
            "next": [
                {
                    "x": 3,
                    "y": 0
                }
            ],
            "type": 4096,
            "refresh": "@refresh"
        },
        "201": {
            "index": "201",
            "pos": {
                "x": 2,
                "y": 1
            },
            "next": [
                {
                    "x": 3,
                    "y": 0
                }
            ],
            "type": 4096,
            "refresh": "@refresh"
        },
        "300": {
            "index": "300",
            "pos": {
                "x": 3,
                "y": 0
            },
            "next": [],
            "type": 1048576,
            "zone_end": True
        }
    }
}

