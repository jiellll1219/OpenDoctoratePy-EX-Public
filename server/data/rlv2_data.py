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

test_data = lambda zone:{
            "1": {
                "id": "zone_1",
                "type": 0,
                "variation": [],
                "index": "1",
                "nodes": {
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
                            }
                        ],
                        "type": 0,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
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
                                "y": 1
                            }
                        ],
                        "type": 1,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        },
                        "stage": f"ro{zone}_n_1_1"
                    },
                    "2": {
                        "index": "2",
                        "pos": {
                            "x": 0,
                            "y": 2
                        },
                        "next": [
                            {
                                "x": 1,
                                "y": 2
                            }
                        ],
                        "type": 2,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        },
                        "stage": f"ro{zone}_e_1_1"
                    },
                    "3": {
                        "index": "3",
                        "pos": {
                            "x": 0,
                            "y": 3
                        },
                        "next": [
                            {
                                "x": 1,
                                "y": 3
                            }
                        ],
                        "type": 4,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        },
                        "stage": f"ro{zone}_b_1"
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
                            }
                        ],
                        "type": 8,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
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
                                "y": 1
                            }
                        ],
                        "type": 16,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
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
                                "y": 2
                            }
                        ],
                        "type": 32,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
                    },
                    "103": {
                        "index": "103",
                        "pos": {
                            "x": 1,
                            "y": 3
                        },
                        "next": [
                            {
                                "x": 2,
                                "y": 3
                            }
                        ],
                        "type": 64,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
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
                        "type": 128,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
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
                                "y": 1
                            }
                        ],
                        "type": 256,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
                    },
                    "202": {
                        "index": "202",
                        "pos": {
                            "x": 2,
                            "y": 2
                        },
                        "next": [
                            {
                                "x": 3,
                                "y": 2
                            }
                        ],
                        "type": 512,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
                    },
                    "203": {
                        "index": "203",
                        "pos": {
                            "x": 2,
                            "y": 3
                        },
                        "next": [
                            {
                                "x": 3,
                                "y": 3
                            }
                        ],
                        "type": 1024,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
                    },
                    "300": {
                        "index": "300",
                        "pos": {
                            "x": 3,
                            "y": 0
                        },
                        "next": [
                            {
                                "x": 4,
                                "y": 0
                            }
                        ],
                        "type": 2048,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
                    },
                    "301": {
                        "index": "301",
                        "pos": {
                            "x": 3,
                            "y": 1
                        },
                        "next": [
                            {
                                "x": 4,
                                "y": 1
                            }
                        ],
                        "type": 4096,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
                    },
                    "302": {
                        "index": "302",
                        "pos": {
                            "x": 3,
                            "y": 2
                        },
                        "next": [
                            {
                                "x": 4,
                                "y": 2
                            }
                        ],
                        "type": 8192,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
                    },
                    "303": {
                        "index": "303",
                        "pos": {
                            "x": 3,
                            "y": 3
                        },
                        "next": [
                            {
                                "x": 4,
                                "y": 3
                            }
                        ],
                        "type": 16384,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
                    },
                    "400": {
                        "index": "400",
                        "pos": {
                            "x": 4,
                            "y": 0
                        },
                        "next": [
                            {
                                "x": 5,
                                "y": 0
                            }
                        ],
                        "type": 32768,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
                    },
                    "401": {
                        "index": "401",
                        "pos": {
                            "x": 4,
                            "y": 1
                        },
                        "next": [
                            {
                                "x": 5,
                                "y": 1
                            }
                        ],
                        "type": 65536,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
                    },
                    "402": {
                        "index": "402",
                        "pos": {
                            "x": 4,
                            "y": 2
                        },
                        "next": [
                            {
                                "x": 5,
                                "y": 2
                            }
                        ],
                        "type": 131072,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
                    },
                    "403": {
                        "index": "403",
                        "pos": {
                            "x": 4,
                            "y": 3
                        },
                        "next": [
                            {
                                "x": 5,
                                "y": 3
                            }
                        ],
                        "type": 262144,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
                    },
                    "500": {
                        "index": "500",
                        "pos": {
                            "x": 5,
                            "y": 0
                        },
                        "next": [
                            {
                                "x": 6,
                                "y": 0
                            }
                        ],
                        "type": 524288,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
                    },
                    "501": {
                        "index": "501",
                        "pos": {
                            "x": 5,
                            "y": 1
                        },
                        "next": [
                            {
                                "x": 6,
                                "y": 0
                            }
                        ],
                        "type": 1048576,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
                    },
                    "502": {
                        "index": "502",
                        "pos": {
                            "x": 5,
                            "y": 2
                        },
                        "next": [
                            {
                                "x": 6,
                                "y": 0
                            }
                        ],
                        "type": 7,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
                    },
                    "503": {
                        "index": "503",
                        "pos": {
                            "x": 5,
                            "y": 3
                        },
                        "next": [
                            {
                                "x": 6,
                                "y": 0
                            }
                        ],
                        "type": 913136,
                        "refresh": {
                            "usedCount": 0,
                            "count": 99,
                            "cost": 1
                        }
                    },
                    "600": {
                        "index": "600",
                        "pos": {
                            "x": 6,
                            "y": 0
                        },
                        "next": [
                            {
                                "x": 7,
                                "y": 0
                            }
                        ],
                        "type": 1965816
                    },
                    "700": {
                        "index": "700",
                        "pos": {
                            "x": 7,
                            "y": 0
                        },
                        "next": [],
                        "type": 1965823,
                        "zone_end": True
                    }
                }
            }
        }